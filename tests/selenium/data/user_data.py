LOGIN_USERS = {
    "register_user":("user02", "Aa@123456", "Aa@123456"),
    "valid_user": ("user06", "Aa@123456"),
    "valid_user_3":("user03", "Aa@123456"),
    "not_exist_user": ("user08", "Aa@123456"),
    "wrong_password": ("user02", "Aa@678912"),
    "wrong_both": ("us", "Aa@678912"),
    "empty_username": ("", "Aa@123456"),
    "empty_password": ("user02", ""),
}

REGISTER_USERS = {
    "valid": ("user01", "Aa@123456", "Aa@123456"),
    "empty_username": ("", "Aa@123456", "Aa@123456"),
    "username_space": ("us er02", "Aa@123456", "Aa@123456"),
    "username_too_long": ("a" * 31, "Aa@123456", "Aa@123456"),
    "username_too_short": ("us", "Aa@123456", "Aa@123456"),
    "duplicate_username": ("user01", "Aa@123456", "Aa@123456"),
    "empty_password": ("user02", "", "Aa@123456"),
    "missing_uppercase": ("user02", "aa@123456", "aa@123456"),
    "missing_lowercase": ("user02", "AA@123456", "AA@123456"),
    "missing_number": ("user02", "Aa@aaaaa", "Aa@aaaaa"),
    "missing_special": ("user02", "Aaa123456", "Aaa123456"),
    "password_space": ("user02", " Aa@123456", " Aa@123456"),
    "password_too_short": ("user02", "Aa@123", "Aa@123"),
    "password_too_long": ("user02", "A" + ("a" * 20) + "@0123456789", "A" + ("a" * 20) + "@0123456789"),
    "empty_confirm": ("user02", "Aa@123456", ""),
    "confirm_not_match": ("user02", "Aa@123456", "Aacde123"),
    "all_invalid": ("ue 01", "A@123456", "Aa@123"),

    "valid_user": [
        ("user03", "Aa@123456", "Aa@123456"),
        ("user04", "Aa@123456", "Aa@123456"),
        ("user05", "Aa@123456", "Aa@123456"),
        ("user06", "Aa@123456", "Aa@123456"),
    ]
}