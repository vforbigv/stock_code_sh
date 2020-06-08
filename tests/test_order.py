#!/usr/bin/env python3
"""pyetrade authorization unit tests
   TODO:
       * Test request error
       * Test API URL"""

import unittest
from unittest.mock import patch
from pyetrade import order
from collections import OrderedDict


class TestETradeOrder(unittest.TestCase):
    """TestEtradeOrder Unit Test"""

    @patch("pyetrade.order.OAuth1Session")
    def test_list_orders(self, MockOAuthSession):
        """test_place_equity_order(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session"""
        # Set Mock returns
        MockOAuthSession().get().json.return_value = "{'accountId': '12345'}"
        MockOAuthSession().get().text = r"<xml> returns </xml>"
        orders = order.ETradeOrder(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )
        # Test Dev buy order equity
        self.assertEqual(orders.list_orders("12345"), "{'accountId': '12345'}")
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)
        # Test Prod buy order equity
        self.assertEqual(orders.list_orders("12345"), "{'accountId': '12345'}")
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)
        self.assertEqual(
            orders.list_orders("12345", resp_format="xml"), r"<xml> returns </xml>"
        )
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)

    # Mock out OAuth1Session
    @patch("pyetrade.order.OAuth1Session")
    def test_place_equity_order(self, MockOAuthSession):
        """test_place_equity_order(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session"""
        # Set Mock returns
        ret_val = r"<PreviewOrderResponse><PreviewIds><previewId>321</previewId></PreviewIds></PreviewOrderResponse>"
        MockOAuthSession().post().text = r"<PreviewOrderResponse><PreviewIds><previewId>321</previewId></PreviewIds></PreviewOrderResponse>"
        orders = order.ETradeOrder(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )
        # Test xml buy order equity
        self.assertEqual(
            orders.place_equity_order(
                resp_format="xml",
                accountId="12345",
                symbol="ABC",
                orderAction="BUY",
                clientOrderId="1a2b3c",
                priceType="MARKET",
                quantity=100,
                orderTerm="GOOD_UNTIL_CANCEL",
                marketSession="REGULAR",
            ),
            ret_val,
        )
        # self.assertTrue(MockOAuthSession().post().json.called)
        self.assertTrue(MockOAuthSession().post.called)
        # Test OrderedDict buy order equity
        self.assertEqual(
            orders.place_equity_order(
                accountId="12345",
                symbol="ABC",
                orderAction="BUY",
                clientOrderId="1a2b3c",
                priceType="MARKET",
                quantity=100,
                orderTerm="GOOD_UNTIL_CANCEL",
                marketSession="REGULAR",
            )["PreviewOrderResponse"]["PreviewIds"]["previewId"],
            "321",
        )
        self.assertTrue(MockOAuthSession().post.called)
        # Test json buy order equity
        ret_val = {"PreviewOrderResponse": {"PreviewIds": {"previewId": 321}}}

        MockOAuthSession().post().json.return_value = ret_val
        self.assertEqual(
            orders.place_equity_order(
                resp_format="json",
                accountId="12345",
                symbol="ABC",
                orderAction="BUY",
                clientOrderId="1a2b3c",
                priceType="MARKET",
                quantity=100,
                orderTerm="GOOD_UNTIL_CANCEL",
                marketSession="REGULAR",
            ),
            ret_val,
        )
        self.assertTrue(MockOAuthSession().post().json.called)
        self.assertTrue(MockOAuthSession().post.called)

    @patch("pyetrade.order.OAuth1Session")
    def test_place_equity_order_exception(self, MockOAuthSession):
        """test_place_equity_order_exception(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session"""
        orders = order.ETradeOrder(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )

        # Test exception class
        with self.assertRaises(order.OrderException):
            orders.place_equity_order()
        try:
            orders.place_equity_order()
        except order.OrderException as e:
            print(e)
        # Test STOP
        with self.assertRaises(order.OrderException):
            orders.place_equity_order(
                accountId="12345",
                symbol="ABC",
                orderAction="BUY",
                clientOrderId="1a2b3c",
                priceType="STOP",
                quantity=100,
                orderTerm="GOOD_UNTIL_CANCEL",
                marketSession="REGULAR",
            )
        # Test LIMIT
        with self.assertRaises(order.OrderException):
            orders.place_equity_order(
                accountId="12345",
                symbol="ABC",
                orderAction="BUY",
                clientOrderId="1a2b3c",
                priceType="LIMIT",
                quantity=100,
                orderTerm="GOOD_UNTIL_CANCEL",
                marketSession="REGULAR",
            )
        # Test STOP_LIMIT
        with self.assertRaises(order.OrderException):
            orders.place_equity_order(
                accountId="12345",
                symbol="ABC",
                orderAction="BUY",
                clientOrderId="1a2b3c",
                priceType="STOP_LIMIT",
                quantity=100,
                orderTerm="GOOD_UNTIL_CANCEL",
                marketSession="REGULAR",
            )
        # Test Prod JSON
        # self.assertEqual(orders.place_equity_order(), "{'account': 'abc123'}")
        # Test Dev XML
        # self.assertEqual(orders.place_equity_order(resp_format='xml'), r'<xml> returns </xml>')
        # self.assertTrue(MockOAuthSession().get().text.called)

    @patch("pyetrade.order.OAuth1Session")
    def test_cancel_order(self, MockOAuthSession):
        """test_cancel_order(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session"""
        MockOAuthSession().put().json.return_value = "{'accountId': '12345'}"
        MockOAuthSession().put().text = r"<xml> returns </xml>"
        orders = order.ETradeOrder(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )
        # Prod
        self.assertEqual(
            orders.cancel_order("12345", 42, resp_format="json"),
            "{'accountId': '12345'}",
        )
        MockOAuthSession().put.assert_called_with(
            ("https://api.etrade.com/v1/accounts" "/12345/orders/cancel"),
            json={"CancelOrderRequest": {"orderId": 42}},
            timeout=30,
        )
        self.assertTrue(MockOAuthSession().put().json.called)
        self.assertTrue(MockOAuthSession().put.called)
        self.assertEqual(
            orders.cancel_order("12345", 42, resp_format="xml"), "<xml> returns </xml>"
        )
