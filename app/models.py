from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    full_name = models.CharField("ФИО", max_length=200)
    phone_number = PhoneNumberField("Телефон", region="RU")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self) -> str:
        return self.full_name


class Salon(models.Model):
    title = models.CharField("Название салона", max_length=100)
    address = models.TextField("Адрес салона", max_length=200)
    photo = models.ImageField("Фото салона", null=True, blank=True)

    class Meta:
        verbose_name = "Салон"
        verbose_name_plural = "Салоны"

    def __str__(self) -> str:
        return self.title


class Service(models.Model):
    title = models.CharField("Название услуги", max_length=200)
    price = models.DecimalField(
        "Цена услуги",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    duration = models.PositiveSmallIntegerField("Длительность услуги, мин")
    photo = models.ImageField("Фото услуги", null=True, blank=True)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self) -> str:
        return self.title


class Master(models.Model):
    full_name = models.CharField("ФИО", max_length=200)
    specialty = models.CharField("Специальность", max_length=200)
    photo = models.ImageField("Фото мастера", null=True, blank=True)

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

    def __str__(self) -> str:
        return f"{self.full_name} {self.specialty}"


class MasterDaySchedule(models.Model):
    workday = models.DateField("Дата")
    salon = models.ForeignKey(
        Salon,
        related_name="schedules",
        on_delete=models.PROTECT,
        verbose_name="Салон",
    )
    master = models.ForeignKey(
        Master,
        related_name="schedules",
        on_delete=models.PROTECT,
        verbose_name="Мастер",
    )
    services = models.ManyToManyField(
        Service, related_name="schedules", verbose_name="Услуги"
    )
    shift_start = models.TimeField("Время начала смены")
    shift_end = models.TimeField("Время окончания смены")

    class Meta:
        verbose_name = "Расписание мастера"
        verbose_name_plural = "Расписания мастеров"

    def __str__(self) -> str:
        return f"{self.master} {self.salon} {self.workday}"


class Invoice(models.Model):
    STATUS = [
        ("not_paid", "Неоплачено"),
        ("paid", "Оплачено"),
    ]
    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, verbose_name="Клиент"
    )
    status = models.CharField("Статус счета", max_length=20, choices=STATUS)
    created_at = models.DateTimeField("Счёт выставлен", auto_now_add=True)
    updated_at = models.DateTimeField("Счёт обновлен", auto_now=True)

    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"

    def __str__(self) -> str:
        return f"{self.updated_at} {self.client.full_name} {self.status}"


class Order(models.Model):
    STATUSES = [
        ("accepted", "Принята"),
        ("ended", "Завершена"),
        ("discard", "Отменена"),
    ]
    status = models.CharField("Статус записи", max_length=20, choices=STATUSES)
    date = models.DateField("Дата записи")
    salon = models.ForeignKey(
        Salon,
        related_name="orders",
        on_delete=models.PROTECT,
        verbose_name="Салон",
    )
    client = models.ForeignKey(
        Client,
        related_name="orders",
        on_delete=models.PROTECT,
        verbose_name="Клиент",
    )
    master = models.ForeignKey(
        Master,
        related_name="orders",
        on_delete=models.PROTECT,
        verbose_name="Мастер",
    )
    service = models.ForeignKey(
        Service,
        related_name="orders",
        on_delete=models.PROTECT,
        verbose_name="Услуга",
    )
    start_at = models.TimeField("Время начала")
    invoice = models.OneToOneField(
        Invoice, on_delete=models.PROTECT, verbose_name="Счет"
    )

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self) -> str:
        return f"{self.status} {self.date} {self.salon.title} {self.client.full_name}"


class Feedback(models.Model):
    date = models.DateField("Дата посещения салона")
    client = models.ForeignKey(
        Client,
        related_name="feedbacks",
        on_delete=models.PROTECT,
        verbose_name="Клиент",
    )
    comment = models.TextField("Текст отзыва")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self) -> str:
        return f"{self.date} {self.client}"
