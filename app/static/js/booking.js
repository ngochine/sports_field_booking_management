function cancelBooking(bookingId){
    fetch(`/api/bookings/${bookingId}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        },
        credentials: 'include',
        body: JSON.stringify({ 
            "status": "CANCELLED"
        })
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => { throw err })
        }
        return res.json()
    })
    .then(data => {
        alert("Huỷ sân thành công!")
        window.location.href = "/bookings"
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


function payBooking(bookingId){
    fetch(`/api/transaction/pay`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        credentials: 'include',
        body: JSON.stringify({
            "booking_id": bookingId
        })
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => { throw err })
        }
        return res.json()
    })
    .then(data => {
        window.location.href = data.payment_url
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