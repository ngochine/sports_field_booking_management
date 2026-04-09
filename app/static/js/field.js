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