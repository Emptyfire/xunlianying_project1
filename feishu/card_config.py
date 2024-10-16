#feishu/card_config.py

#内容
image1 = ""
staplefood = "米"
staplefood_amount = "100g"
meet = "肉"
meet_amount = "100/100g"
meet2 = "肉"
meet2_amount = "22/22g"
veggie = "菜"
carbohydrates_today = "120g"
protein_today = "120g"
axunge_today = "120g"
carbohydrates = "100g"
protein = "100g"
axunge = "100g"
selfevaluation = "说实话这餐不太行的，里面还有禁忌食物牛肉丸，但是主要是为了空冰箱，把之前冰箱里的乱七八糟的东西吃一吃，所以也算没什么办法的事情"
staff = "<at id=ou_3a42f5e5e8dc9b9deb0248640152416c></at> <at id=ou_3a42f5e5e8dc9b9deb0248640152416c></at> <at id=ou_3a42f5e5e8dc9b9deb0248640152416c></at>"

# title
group_name = "A组"
name = "22"
tree = "早餐"
record = "1"
Date = "2022-1-4"


card = {
    "config": {
        "update_multi": True
    },
    "i18n_elements": {
        "zh_cn": [
            {
                "tag": "img",
                "img_key": "img_v3_02fh_1f7ad0d2-1a7c-472e-9e1b-001d56e862fg",
                "preview": True,
                "transparent": False,
                "scale_type": "fit_horizontal",
                "alt": {
                    "tag": "plain_text",
                    "content": ""
                }
            },
            {
                "tag": "markdown",
                "content": f"{staplefood}{staplefood_amount}  {meet}{meet_amount}  {meet2}{meet2_amount} {veggie}",
                "text_align": "center",
                "text_size": "heading"
            },
            {
                "tag": "hr"
            },
            {
                "tag": "markdown",
                "content": "**今日营养素配额情况**",
                "text_align": "center",
                "text_size": "heading"
            },
            {
                "tag": "column_set",
                "flex_mode": "none",
                "horizontal_spacing": "8px",
                "horizontal_align": "left",
                "columns": [
                    {
                        "tag": "column",
                        "width": "weighted",
                        "vertical_align": "top",
                        "vertical_spacing": "8px",
                        "elements": [
                            {
                                "tag": "markdown",
                                "content": f"**今日碳水**\n{carbohydrates_today}",
                                "text_align": "center",
                                "text_size": "normal"
                            }
                        ],
                        "weight": 1
                    },
                    {
                        "tag": "column",
                        "width": "weighted",
                        "vertical_align": "top",
                        "vertical_spacing": "8px",
                        "elements": [
                            {
                                "tag": "markdown",
                                "content": f"**今日蛋白质**\n{protein_today}",
                                "text_align": "center",
                                "text_size": "normal"
                            }
                        ],
                        "weight": 1
                    },
                    {
                        "tag": "column",
                        "width": "weighted",
                        "vertical_align": "top",
                        "vertical_spacing": "8px",
                        "elements": [
                            {
                                "tag": "markdown",
                                "content": f"**今日脂肪**\n{axunge_today}",
                                "text_align": "center",
                                "text_size": "normal"
                            }
                        ],
                        "weight": 1
                    }
                ],
                "margin": "16px 0px 0px 0px"
            },
            {
                "tag": "column_set",
                "flex_mode": "none",
                "horizontal_spacing": "8px",
                "horizontal_align": "left",
                "columns": [
                    {
                        "tag": "column",
                        "width": "weighted",
                        "vertical_align": "top",
                        "vertical_spacing": "8px",
                        "elements": [
                            {
                                "tag": "markdown",
                                "content": f"**本餐碳水**\n{carbohydrates}",
                                "text_align": "center",
                                "text_size": "normal"
                            }
                        ],
                        "weight": 1
                    },
                    {
                        "tag": "column",
                        "width": "weighted",
                        "vertical_align": "top",
                        "vertical_spacing": "8px",
                        "elements": [
                            {
                                "tag": "markdown",
                                "content": f"**本餐蛋白质**\n{protein}",
                                "text_align": "center",
                                "text_size": "normal"
                            }
                        ],
                        "weight": 1
                    },
                    {
                        "tag": "column",
                        "width": "weighted",
                        "vertical_align": "top",
                        "vertical_spacing": "8px",
                        "elements": [
                            {
                                "tag": "markdown",
                                "content": f"**本餐脂肪**\n{axunge}",
                                "text_align": "center",
                                "text_size": "normal"
                            }
                        ],
                        "weight": 1
                    }
                ],
                "margin": "16px 0px 0px 0px"
            },
            {
                "tag": "hr"
            },
            {
                "tag": "markdown",
                "content": "**自评**",
                "text_align": "center",
                "text_size": "normal"
            },
            {
                "tag": "markdown",
                "content": f"{selfevaluation}",
                "text_align": "left",
                "text_size": "notation"
            },
            {
                "tag": "hr"
            },
            {
                "tag": "markdown",
                "content": f"{staff}",
                "text_align": "center",
                "text_size": "normal"
            },
        ]
    },
    "i18n_header": {
        "zh_cn": {
            "title": {
                "tag": "plain_text",
                "content": f"{group_name}/{name}/{tree}/{record}"
            },
            "subtitle": {
                "tag": "plain_text",
                "content": f"{Date}"
            },
            "template": "red"
        },
        
    }
}

