from abc import ABC, abstractmethod
from .models import Alarm

# Subject 클래스
class CategoryNotifier:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, observer):
        self.subscribers.append(observer)

    def unsubscribe(self, observer):
        self.subscribers.remove(observer)

    def notify_subscribers(self, users, post, message):
        print(f"Notifier: Notifying {len(users)} subscribers.")
        for observer in self.subscribers:
            observer.update(users, post, message)


# Observer 인터페이스
class Observer(ABC):
    @abstractmethod
    def update(self, users, post, message):
        pass


# 이메일 알림
class EmailAlarm(Observer):
    def update(self, users, post, message):
        pass


class LoggingAlarm(Observer):
    def update(self, users, post, message):
        for user in users:
            # 새로운 알림을 저장
            print(f"Creating alarm for user: {user.username} with message: {message}")
            Alarm.objects.create(
                user=user,
                post=post,
                message=message,
            )




