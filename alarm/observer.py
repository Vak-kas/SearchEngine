from abc import ABC, abstractmethod

# Subject 클래스
class CategoryNotifier:
    def __init__(self):
        self.subscribers = []  # 구독자 목록

    def subscribe(self, observer):
        self.subscribers.append(observer)

    def unsubscribe(self, observer):
        self.subscribers.remove(observer)

    def notify_subscribers(self, users, post, message):
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
        for user in users:
            if user.email:
                print(f"Email sent to {user.email}: {message}")


# 로깅 알림 (예: 프론트에 실시간 알림 표시용)
class LoggingAlarm(Observer):
    def update(self, users, post, message):
        for user in users:
            print(f"Log for {user.username}: {message}")
