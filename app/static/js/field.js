function getCity(selectedCity) {
    fetch("https://provinces.open-api.vn/api/v2/?depth=1")
        .then(res => {
            if (!res.ok) throw new Error("API lỗi")
            return res.json()
        })
        .then(data => {
            const select = document.getElementById("citySearch")

            data.forEach(city => {
                const option = document.createElement("option")
                option.value = city.code
                option.textContent = city.name

                if (selectedCity == city.code) {
                    option.selected = true;
                }

                select.appendChild(option)
            })
        })
        .catch(err => {
            console.log(err)
        })
}


function getDistrict(cityCode, selectedDistrict) {
    fetch(`https://provinces.open-api.vn/api/p/${cityCode}?depth=2`)
        .then(res => {
            if (!res.ok) throw new Error("API lỗi")
            return res.json()
        })
        .then(data => {
            const select = document.getElementById("districtsSearch")
            select.innerHTML = '<option value="">Chọn Quận/Huyện</option>'

            if (data.districts) {
                data.districts.forEach(district => {
                    const option = document.createElement("option")
                    option.value = district.code
                    option.textContent = district.name

                    if (selectedDistrict == district.code) {
                        option.selected = true;
                    }

                    select.appendChild(option)
                })
            }
        })
        .catch(err => {
            console.error(err)
        });
}


//detail
function validateDate(input) {
    if (!input.value) return;
    const selectedDate = new Date(input.value);
    const minDate = new Date(input.min);
    selectedDate.setHours(0, 0, 0, 0);
    minDate.setHours(0, 0, 0, 0);
    if (selectedDate < minDate) {
        alert("Không được chọn ngày ở quá khứ");
        input.value = input.min;
    }
}


function loadFieldPrice(fieldId, dateSelected){
    fetch(`/api/fields/${fieldId}/field-price?date=${dateSelected}`)
        .then(res => {
            if (!res.ok) throw new Error("API lỗi")
            return res.json()
        })
        .then(data => {
            let html = ""
            if (data.field_prices.length > 0){
                html += `
                    <div class="col-12">
                        <div class="table-responsive">
                            <table class="table table-hover align-middle text-center">
                                <thead>
                                    <tr>
                                        <th style="color: var(--blue);">Giờ bắt đầu</th>
                                        <th style="color: var(--blue);">Giờ kết thúc</th>
                                        <th style="color: var(--blue);">Giá</th>
                                    </tr>
                                </thead>
                                <tbody>
                `
                data.field_prices.forEach(f => {
                    html += `
                        <tr>
                            <td>${f.start_time}</td>
                            <td>${f.end_time}</td>
                            <td class="fw-bold" style="color: var(--orange);">
                                ${Number(f.price).toLocaleString("vi-VN")} VNĐ
                            </td>
                        </tr>
                    `
                })
                html += `
                                </tbody>
                            </table>
                        </div>
                    </div>
                `
            } else {
                html = `
                    <div class="col-12 small text-muted">
                        Hiện sân chưa có lịch hoạt động.
                    </div>
                `
            }
            document.getElementById("fieldPriceContainer").innerHTML = html
        })
        .catch(err => {
            container.innerHTML = ""
            handleMessages(container, err)
        })
}


function loadConfirmBooking(){
    document.getElementById("confirmDate").innerHTML = document.getElementById("dateSelectedValue").value
    document.getElementById("confirmStartTime").innerHTML = document.getElementById("startTime").value
    document.getElementById("confirmEndTime").innerHTML = document.getElementById("endTime").value
    document.getElementById("confirmDuration").innerHTML = document.getElementById("totalTime").textContent + " Giờ"
    document.getElementById("confirmTotalPrice").innerHTML = document.getElementById("totalPrice").textContent + " VND"
}


function caculatorTotalBooking(fieldId){
    document.getElementById("errMessage").innerHTML = ""
    const bookingDate = document.getElementById("dateSelectedValue").value
    const startTime = document.getElementById("startTime").value
    const endTime = document.getElementById("endTime").value

    if (!startTime || !endTime){
        document.getElementById("btnCreateBooking").disabled = true
        return
    }

    fetch("/api/bookings/calculate-price", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "field_id": fieldId,
            "booking_date": bookingDate,
            "start_time": startTime,
            "end_time": endTime
        })
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => { throw err })
        }
        return res.json()
    })
    .then(data => {
        document.getElementById("totalTime").innerHTML = data.total_time
        document.getElementById("totalPrice").innerHTML = data.total_price.toLocaleString("vi-VN")
        document.getElementById("btnCreateBooking").disabled = false
    })
    .catch(err => {
        document.getElementById("totalTime").innerHTML = 0
        document.getElementById("totalPrice").innerHTML = 0
        document.getElementById("btnCreateBooking").disabled = true
        document.getElementById("errMessage").innerHTML = "Sân hiện không phục vụ trong khung giờ bạn chọn. Vui lòng chọn khung giờ khác."
    })
}


function createBooking(fieldId){
    dataSelected = document.getElementById("dateSelectedValue").value
    startTime = document.getElementById("startTime").value
    endTime = document.getElementById("endTime").value

    fetch(`/api/fields/${fieldId}/booking`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        credentials: 'include',
        body: JSON.stringify({ 
            "booking_date": dataSelected, 
            "start_time": startTime, 
            "end_time": endTime
        })
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => { throw err })
        }
        return res.json()
    })
    .then(data => {
        alert("Đặt sân thành công!")
        setTimeout(() => window.location.href = "/bookings", 500)
    })
    .catch(err => {
        console.log(err)
        let messages = []
        if (typeof err.message === "object") {
            Object.values(err.message)
                .forEach(msgArr => {
                    if (Array.isArray(msgArr)) {
                        messages.push(...msgArr)
                    } else {
                        messages.push(msgArr)
                    }
                })
        } else {
            messages.push(
                err.message || "Có lỗi xảy ra"
            )
        }
        alert(messages.join("\n"))
    })
}