function showAlert(container, message, category) {
    container.insertAdjacentHTML('beforeend', `
        <div class="alert alert-${category} m-3 alert-dismissible fade show position-relative" style="z-index: 99999;">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `)
}


function handleMessages(container, data, type = "danger") {
    const messages = typeof data.message === "object"
        ? Object.values(data.message).flat()
        : [data.message]

    messages.forEach(m => showAlert(container, m, type))
}


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


function createBooking(fieldId){
    dataSelected = document.getElementById("dateSelectedValue").value
    startTime = document.getElementById("startTime").value
    endTime = document.getElementById("endTime").value
    const container = document.getElementById("flash-container")

    fetch(`/api/fields/${fieldId}/booking`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        credentials: 'include',
        body: JSON.stringify({ dataSelected, startTime, endTime})
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => { throw err })
        }
        return res.json()
    })
    .then(data => {
        container.innerHTML = ""
        showAlert(container, "Đặt sân thành công", "success")
        setTimeout(() => window.location.href = "/history-booking", 500)
    })
    .catch(err => {
        container.innerHTML = ""
        handleMessages(container, err)
    })
}