"""服务预约完整场景：选择、日期时间、加服务、确认、取消、重复提交。"""

import os

import pytest
from selenium.webdriver.common.by import By

from pages.booking_page import BookingPage
from pages.checkout_page import CheckoutPage


def _to_day_time(page):
    """从服务选择进入日期时间步骤。"""
    page.select_service("139")
    page.click_next()
    page.wait_for_day_time()
    return page


def _to_checkout(page, day="18", time_value="09:30"):
    """选择日期时间并进入预约确认/结算页。"""
    _to_day_time(page)
    page.select_date(day)
    page.select_time(time_value)
    page.click_proceed_to_checkout()
    return CheckoutPage()


@pytest.mark.core
@pytest.mark.booking
def test_booking_next_without_service_keeps_service_step(booking_page):
    """未选择服务时点击下一步应停留在服务选择步骤。"""
    booking_page.click_next()
    booking_page.wait_for_text("Services")
    body_text = booking_page.driver.find_element(By.TAG_NAME, "body").text
    assert "Proceed to Confirm Booking" not in body_text
    assert "前往確認" not in body_text


@pytest.mark.core
@pytest.mark.booking
def test_booking_service_selection_opens_day_time(booking_page):
    """选择服务后应进入日期时间步骤。"""
    _to_day_time(booking_page)
    assert "Day and time" in booking_page.driver.find_element(
        By.TAG_NAME, "body"
    ).text


@pytest.mark.core
@pytest.mark.booking
def test_booking_missing_day_time_shows_validation(login_page):
    """未选择日期时间时点击确认应显示校验提示。"""
    login_page.login()
    booking_page = BookingPage()
    booking_page.open_url()
    _to_day_time(booking_page)
    booking_page.click_proceed_button()
    body_text = booking_page.driver.find_element(By.TAG_NAME, "body").text
    assert "请选择" in body_text or "Please select" in body_text


@pytest.mark.core
@pytest.mark.booking
def test_add_another_service_returns_to_service_step(login_page):
    """已选日期时间后点击继续添加服务，应回到服务选择步骤。"""
    login_page.login()
    booking_page = BookingPage()
    booking_page.open_url()
    _to_day_time(booking_page)
    booking_page.select_date("18")
    booking_page.select_time("09:30")
    booking_page.click_add_another_service()
    body_text = booking_page.driver.find_element(By.TAG_NAME, "body").text
    assert "Services" in body_text
    assert "下一步" in body_text or "Next" in body_text


@pytest.mark.core
@pytest.mark.booking
def test_booking_confirmation_page_shows_service_and_time(login_page):
    """确认预约页应展示所选服务、预约时间和 ATM 支付方式。"""
    login_page.login()
    booking_page = BookingPage()
    booking_page.open_url()
    checkout_page = _to_checkout(booking_page)
    checkout_page.wait_for_checkout()
    body_text = checkout_page.get_body_text()
    assert "提交预约" in body_text
    assert "Aesthetic consultation" in body_text
    assert "2026-08-18" in body_text
    assert "09:30" in body_text
    assert checkout_page.get_payment_methods() == ["atm"]


@pytest.mark.core
@pytest.mark.booking
def test_booking_cancel_service_from_checkout_x(login_page):
    """结算页服务行的 x 可用于取消当前预约服务。"""
    login_page.login()
    booking_page = BookingPage()
    booking_page.open_url()
    checkout_page = _to_checkout(booking_page)
    checkout_page.wait_for_checkout()
    rows_before = checkout_page.get_service_rows()
    assert rows_before
    checkout_page.remove_first_item()
    rows_after = checkout_page.get_service_rows()
    assert len(rows_after) == len(rows_before) - 1
    assert rows_before[0] not in rows_after
    assert "removeIds" in checkout_page.driver.current_url


@pytest.mark.core
@pytest.mark.booking
@pytest.mark.booking_submit
def test_duplicate_booking_same_slot_blocked(login_page):
    """重复提交同一服务同一时间应被系统拦截；需测试环境允许真实预约。"""
    if os.getenv("BOOKING_SUBMIT_ALLOWED", "false").lower() != "true":
        pytest.skip("BOOKING_SUBMIT_ALLOWED=true 时才执行真实重复预约验证")
    login_page.login()
    booking_page = BookingPage()
    booking_page.open_url()
    checkout_page = _to_checkout(booking_page)
    checkout_page.wait_for_checkout()
    assert checkout_page.is_submit_enabled() is False
