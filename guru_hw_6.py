from datetime import date, datetime




test_emails = [
    "user@gmail.com"
    "admin@company.ru",
    "test_123@service.net",
    "Example.User@domain.com",
    "default@study.com",
    " hello@corp.ru  ",
    "user@site.NET",
    "user@domain.coM",
    "user.name@domain.ru",
    "usergmail.com",
    "user@domain",
    "user@domain.org",
    "@mail.ru",
    "name@.com",
    "name@domain.comm",
    "",
    "   ",
]




def normalize_addresses(value: str) -> str:
    """
    Возвращает значение, в котором адрес приведен к нижнему регистру и очищен от пробелов по краям.
    """
    return value.lower().strip()


def add_short_body(email: dict) -> dict:
    """
    Возвращает email с новым ключом email["short_body"] —
    первые 10 символов тела письма + "...".
    """
    email["short_body"]  = email["body"][:10] + "..."
    return email["short_body"]


def clean_body_text(body: str) -> str:
    """
    Заменяет табы и переводы строк на пробелы.
    """
    body = body.replace("\n", " ").replace("\t", " ")
    return body



def build_sent_text(email: dict) -> str:
    """
    Формирует текст письма в формате:

    Кому: {to}, от {from}
    Тема: {subject}, дата {date}
    {clean_body}
    """
    return (
        f"Кому: {email['recipient']}, от: {email['sender']}\n"
        f"Тема: {email['subject']}, дата: {email['date']}\n"
        f"{email['body']}"
    )


def check_empty_fields(subject: str, body:str) -> tuple[bool, bool]:
    """
    Возвращает кортеж (is_subject_empty, is_body_empty).
    True, если поле пустое.
    """
    is_subject_empty = subject.strip() == ""
    is_body_empty = body.strip() == ""
    return is_subject_empty, is_body_empty


def mask_sender_email(login: str, domain: str) -> str:
    """
    Возвращает маску email: первые 2 символа логина + "***@" + домен.
    """
    masked_email = login[:2] + "***@" + domain
    return masked_email




def get_correct_email(email_list: list[str]) -> list[str]:
    """
    Возвращает список корректных email.
    """
    correct_domains = ['.com', '.ru', '.net']
    result = []
    for email in email_list:
        if '.' in email and '@' in email:
            domain= email[(email.rindex('.')):].strip()
            if domain in correct_domains and email.count('@') == 1:
                result.append(email)

    return result

def create_email(sender: str, recipient: str, subject: str, body: str) -> dict:
    """
    Создает словарь email с базовыми полями:
    'sender', 'recipient', 'subject', 'body'
    """
    return {
        "sender": sender,
        "recipient": recipient,
        "subject": subject,
        "body": body
    }



def add_send_date(email: dict) -> dict:
    """
    Возвращает email с добавленным ключом email["date"] — текущая дата в формате YYYY-MM-DD.
    """
    send_date = datetime.now().strftime("%Y-%m-%d")
    email["date"] = send_date
    return email


def extract_login_domain(address: str) -> tuple[str, str]:
    """
    Возвращает логин и домен отправителя.
    Пример: "user@mail.ru" -> ("user", "mail.ru")
    """
    # 4. Извлеките логин и домен отправителя в две переменные login и domain.
    at_index = address.index('@')
    login = address[:at_index]
    domain = address[at_index + 1:]
    return login, domain







def sender_email(recipient_list: list[str], subject: str, message: str, *, sender="default@study.com") -> list[dict]:


    # Проверить, что recipient_list не пустой.
    if not recipient_list:
        raise ValueError("Список получателей не может быть пустым")

    # Проверить корректность email отправителя и получателей через get_correct_email().
    correct_recipient_list = get_correct_email(recipient_list)
    if not correct_recipient_list:
        raise ValueError("Email получателей некорректен")

    check_sender = get_correct_email([sender])
    if not check_sender:
        raise ValueError("Email отправителя некорректен")

    # Проверить пустоту темы и тела письма через check_empty_fields(). Если одно из них пустое — вернуть пустой список.
    is_subject_empty, is_body_empty = check_empty_fields(subject, message)
    if is_subject_empty or is_body_empty:
        return []

    # Исключить отправку самому себе: пройти по каждому элементу recipient_list в цикле for, если адрес совпадает с sender, удалить его из списка.
    for recipient in correct_recipient_list:
        if recipient == sender.strip():
            correct_recipient_list.remove(recipient)


    # Нормализовать: subject и body → с помощью clean_body_text() recipient_list и sender → с помощью normalize_addresses()
    subject = clean_body_text(subject)
    message = clean_body_text(message)

    for index, recipient in enumerate(correct_recipient_list):
        correct_recipient_list[index] = normalize_addresses(recipient)

    sender = normalize_addresses(sender)


    # Создать письмо для каждого получателя функцией create_email().
    emails = []
    for recipient in correct_recipient_list:
        email = create_email(sender, recipient, subject, message)

        # Добавить дату отправки с помощью add_send_date().
        add_send_date(email)

        # Замаскировать email отправителя с помощью extract_login_domain() и mask_sender_email().
        login, domain = extract_login_domain(email["sender"])
        mask_sender_email(login, domain)
        email['masked_sender'] = mask_sender_email(login, domain)

        # Сохранить короткую версию в email["short_body"].
        add_short_body(email)

        # Сформировать итоговый текст письма функцией build_sent_text().
        email["sent_text"] = build_sent_text(email)

        emails.append(email)

    # Вернуть итоговый список писем.
    return emails




print(sender_email(test_emails, 'Тема', 'Hello,\nWe are interested in a partnership.\tPlease reply soon.\nRegards,\nTeam"', sender='sender@study.com'))