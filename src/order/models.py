# Django
from django.db import models


class Order(models.Model):
    """""""""""""""""""""""
    注文情報を扱うクラス
    """""""""""""""""""""""
    class Meta:
        """""""""""""""""""""""""""""
        メタデータ（データの名称）
        """""""""""""""""""""""""""""
        verbose_name = "注文状況"
        verbose_name_plural = "注文"


    class PaymentWay(models.TextChoices):
        """""""""""
        支払方法
        """""""""""
        CASH_ON_DELIVERY = '代金引換', '代金引換'
        BANK_TRANSFER = '銀行振込', '銀行振込'
        CREDIT_CARD = 'クレジットカード', 'クレジットカード'

    class Status(models.IntegerChoices):
        """""""""""""""""""""
        出荷・取引完了情報
        """""""""""""""""""""
        NOT_SHIPPED = 0, '未出荷'
        SHIPPED = 1, '出荷済み'
        COMPLETED = 2, '取引完了'
      
    
    # ユーザー
    user = models.ForeignKey(
      'account.User',
      verbose_name='ユーザー',
      on_delete=models.CASCADE,
      related_name='cart_order'
    )
    # 郵便番号
    postal_code = models.CharField(
        verbose_name='郵便番号',
        max_length=7,
        blank=False
    )
    # 住所
    address = models.CharField(
        verbose_name='住所',
        max_length=255,
        blank=False
    )
    # 支払方法
    payment_way = models.CharField(
        verbose_name='支払方法',
        max_length=8,
        choices=PaymentWay.choices,
        default=PaymentWay.CASH_ON_DELIVERY,
    )
    # 出荷・取引完了情報
    status = models.IntegerField(
        verbose_name='出荷・取引完了情報',
        choices=Status.choices,
        default=Status.NOT_SHIPPED,
    )
    # 追加日時
    created_at = models.DateTimeField(
        verbose_name='追加日時',
        auto_now_add=True
    )
    # 更新日時
    updated_at = models.DateTimeField(
        verbose_name='更新日時',
        auto_now=True
    )

    # 管理サイトで注文情報確認
    def __str__(self):
        return f"≪{self.get_status_display()}≫  [ID: {self.user_id}]  {self.user.email}の注文"


class OrderItem(models.Model):
    """""""""""""""""""""""""""""""""""
    注文内の商品情報を扱うクラス
    """""""""""""""""""""""""""""""""""
    class Meta:
        """""""""""""""""""""""""""""
        メタデータ（データの名称）
        """""""""""""""""""""""""""""
        verbose_name = "注文アイテム"
        verbose_name_plural = "注文アイテム"
    
    # 注文
    order = models.ForeignKey(
      Order,
      verbose_name='注文',
      on_delete=models.CASCADE,
      related_name='order_orderItem'
    )
    product = models.ForeignKey(
        'shop.Product',
        verbose_name='商品',
        on_delete=models.PROTECT  # 注文後に商品削除されても履歴は残す
    )
    product_name = models.CharField(
        verbose_name='商品名',
        max_length=255
    )
    price = models.PositiveIntegerField(
        verbose_name='価格'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='数量'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product_name} x {self.quantity} -> {self.get_total_price()}円"