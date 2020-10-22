from alchemy import COD_User


def load_profile(member: COD_User):
    """показывает профиль пользователя"""

    result = ''
    text0 = "Имя/ник: " + str(member.name) + "\n"
    if member.tg_name != 'unknown':
        text0 += "Имя в Телеге: @" + str(member.tg_name) + "\n"
    text1 = "ACTIVISION ID: " + str(member.activision_id) + "\n"
    text2 = "PSN ID: " + str(member.psn_id) + "\n"
    result += text0 + text1 + text2
    return result


def load_kd(member: COD_User):
    """показывает профиль пользователя"""

    result = ''
    text1 = "К/Д в Варзоне: " + str(member.kd_warzone) + "\n"
    text2 = "К/Д в мультиплеере: " + str(member.kd_multiplayer) + "\n\n"
    text3 = "Last update: " \
            + "\n" + str(member.update_kd.strftime("%d.%m.%Y")) \
            + "\n" + str(member.update_kd.strftime("%H:%M:%S"))
    result += text1 + text2 + text3
    return result
