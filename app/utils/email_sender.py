
async def send_status_update_email(email: str, task_title: str, new_status: str):
    """
    Надсилає електронний лист про оновлення статусу задачі.
    
    - email (str): Електронна пошта отримувача.
    - task_title (str): Назва задачі.
    - new_status (str): Новий статус задачі.
    """
    print(
        f"""Надсилаємо лист на {email}:
        Task Status Update: Task '{task_title}' has been updated to '{new_status}' status."""
    )
    
    # import aiosmtplib
    # from email.mime.text import MIMEText

    # message = MIMEText(f'Task "{task_title}" has been updated to "{new_status}".')
    # message['From'] = "no-reply@yourdomain.com"
    # message['To'] = email
    # message['Subject'] = "Task Status Update"
    
    # await aiosmtplib.send(
    #     message,
    #     hostname="smtp.gmail.com",
    #     port=587,
    #     username="your-gmail-email@gmail.com",
    #     password="your-gmail-app-password",
    #     use_tls=True,
    # )
