document.addEventListener("DOMContentLoaded", function () {
    const provinceSelect = document.getElementById("province_id")
    const districtSelect = document.getElementById("district_id")

    if (!provinceSelect)
        return

    const selectedProvince = provinceSelect.value
    const selectedDistrict = districtSelect.value

    getCity(selectedProvince)

    if (selectedProvince)
        getDistrict(selectedProvince, selectedDistrict)

    provinceSelect.addEventListener("change", function () {
        const provinceName = this.options[this.selectedIndex].text
        document.getElementById("province_name").value = provinceName
        getDistrict(this.value)
    })

    districtSelect.addEventListener("change", function () {
        const districtName = this.options[this.selectedIndex].text
        document.getElementById("district_name").value = districtName
    })
})


function getCity(selectedCity = null) {
    fetch(
        "https://provinces.open-api.vn/api/v2/?depth=1"
    )
    .then(res => {
        if (!res.ok)
            throw new Error("API lỗi")
        return res.json()
    })
    .then(data =>{
        const select = document.getElementById("province_id")
        select.innerHTML ='<option value="">Chọn tỉnh/thành</option>'
        data.forEach(city => {
            const option = document.createElement("option")
            option.value = city.code
            option.textContent = city.name
            if (Number(selectedCity)=== city.code) {
                option.selected = true
            }
            select.appendChild(option)
            })
        })
    .catch(err => {
        console.log(err)
   })
}


function getDistrict(
    cityCode,
    selectedDistrict = null
) {

    fetch(
        `https://provinces.open-api.vn/api/p/${cityCode}?depth=2`
    )

        .then(res => {

            if (!res.ok)
                throw new Error("API lỗi")

            return res.json()
        })

        .then(data => {

            const select =
                document.getElementById(
                    "district_id"
                )

            select.innerHTML =
                '<option value="">Chọn quận/huyện</option>'

            if (data.districts) {

                data.districts.forEach(
                    district => {

                        const option =
                            document.createElement(
                                "option"
                            )

                        option.value =
                            district.code

                        option.textContent =
                            district.name

                        if (
                            Number(
                                selectedDistrict
                            )
                            === district.code
                        ) {

                            option.selected = true
                        }

                        select.appendChild(
                            option
                        )
                    }
                )
            }
        })

        .catch(err => {

            console.error(err)
        })
}