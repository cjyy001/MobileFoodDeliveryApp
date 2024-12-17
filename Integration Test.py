import unittest
from Order_Placement import CartItem, Cart, OrderPlacement, PaymentMethod, UserProfile, RestaurantMenu
from Payment_Processing import PaymentProcessing
from Restaurant_Browsing import RestaurantBrowsing, RestaurantDatabase, RestaurantSearch
from User_Registration import UserRegistration


class TestIntegration(unittest.TestCase):
    def setUp(self):
        # 创建模拟的餐厅数据库
        self.restaurant_db = RestaurantDatabase()

        # 创建餐厅浏览对象
        self.restaurant_browsing = RestaurantBrowsing(self.restaurant_db)

        # 创建餐厅搜索对象
        self.restaurant_search = RestaurantSearch(self.restaurant_browsing)

        # 创建一个模拟的餐厅菜单
        self.restaurant_menu = RestaurantMenu(available_items=['Spaghetti', 'Pizza', 'Lasagna'])

        # 创建一个模拟的用户配置文件
        self.user_profile = UserProfile(delivery_address='123 Main St')

        # 创建购物车对象
        self.cart = Cart()

        # 创建支付处理对象
        self.payment_processing = PaymentProcessing()

    def test_order_process_flow(self):
        # 模拟用户浏览并选择餐厅
        selected_restaurant = self.restaurant_search.search_restaurants(cuisine='Italian', location='Downtown',
                                                                        rating=4.0)
        self.assertGreaterEqual(len(selected_restaurant), 1)

        # 模拟用户添加菜品到购物车
        self.cart.add_item('Spaghetti', 9.99, 2)
        self.cart.add_item('Pizza', 12.99, 1)

        # 模拟用户选择支付方式并支付
        payment_method = 'credit_card'
        payment_details = {'card_number': '1234567890123456', 'expiry_date': '12/24', 'cvv': '123'}
        payment_response = self.payment_processing.process_payment(
            {'total_amount': self.cart.calculate_total()['total']}, payment_method, payment_details)
        self.assertEqual(payment_response, "Payment successful, Order confirmed")

        # 创建订单放置对象
        order_placement = OrderPlacement(self.cart, self.user_profile, self.restaurant_menu)

        # 模拟用户确认订单
        order_confirmation = order_placement.confirm_order(PaymentMethod())
        self.assertTrue(order_confirmation['success'])

    def test_registration(self):
        # 测试用户注册
        registration = UserRegistration(self)
        reg_result = registration.register("newuser@example.com", "SecurePass123", "SecurePass123")
        self.assertTrue(reg_result['success'])

    def test_order_confirmation_failure(self):
        # 测试订单确认失败
        # 假设某些条件下订单确认会失败
        order_placement = OrderPlacement(self.cart, self.user_profile, self.restaurant_menu)
        order_confirmation = order_placement.confirm_order(PaymentMethod())
        self.assertFalse(order_confirmation['success'])


if __name__ == '__main__':
    unittest.main()
