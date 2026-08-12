import pytest
from unittest.mock import Mock
from ..order_tracker import OrderTracker


@pytest.fixture
def mock_storage():
    """
    Provides a mock storage object for tests.
    This mock will be configured to simulate various storage behaviors.
    """
    mock = Mock()
    # By default, mock get_order to return None (no order found)
    mock.get_order.return_value = None
    # By default, mock get_all_orders to return an empty dict
    mock.get_all_orders.return_value = {}
    return mock


@pytest.fixture
def order_tracker(mock_storage):
    """
    Provides an OrderTracker instance initialized with the mock_storage.
    """
    return OrderTracker(mock_storage)


def test_add_order_successfully(order_tracker, mock_storage):
    """Tests adding a new order with default 'pending' status."""
    order_tracker.add_order("ORD001", "Laptop", 1, "CUST001")
    mock_storage.save_order.assert_called_once()
    args = mock_storage.save_order.call_args[0]
    assert args[0] == "ORD001"
    assert args[1]["order_id"] == "ORD001"
    assert args[1]["item_name"] == "Laptop"
    assert args[1]["quantity"] == 1
    assert args[1]["customer_id"] == "CUST001"
    assert args[1]["status"] == "pending"


def test_add_order_raises_error_if_exists(order_tracker, mock_storage):
    """Tests that adding an order with a duplicate ID raises ValueError."""
    mock_storage.get_order.return_value = {"order_id": "ORD_EXISTING"}

    with pytest.raises(
        ValueError,
        match="Order with ID 'ORD_EXISTING' already exists."
    ):
        order_tracker.add_order("ORD_EXISTING", "New Item", 1, "CUST001")


def test_get_order_by_id_successfully(order_tracker, mock_storage):
    """Tests fetching an existing order by its ID."""
    mock_storage.get_order.return_value = {
        "order_id": "ORD001",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "pending"
    }

    result = order_tracker.get_order_by_id("ORD001")
    assert result == mock_storage.get_order.return_value
    mock_storage.get_order.assert_called_with("ORD001")


def test_get_order_by_id_returns_none_if_not_found(
    order_tracker,
    mock_storage
):
    """Tests that fetching a non-existent order returns None."""
    result = order_tracker.get_order_by_id("NON_EXISTENT")
    assert result is None
    mock_storage.get_order.assert_called_with("NON_EXISTENT")


def test_update_order_status_successfully(order_tracker, mock_storage):
    """Tests updating an order's status."""
    mock_storage.get_order.return_value = {
        "order_id": "ORD001",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "pending"
    }

    order_tracker.update_order_status("ORD001", "shipped")
    mock_storage.save_order.assert_called_once()
    args = mock_storage.save_order.call_args[0]
    assert args[0] == "ORD001"
    assert args[1]["status"] == "shipped"


def test_update_order_status_raises_error_if_not_found(
    order_tracker,
    mock_storage
):
    """Tests that updating a non-existent order raises ValueError."""
    mock_storage.get_order.return_value = None

    with pytest.raises(
        ValueError,
        match="Order with ID 'NON_EXISTENT' not found."
    ):
        order_tracker.update_order_status("NON_EXISTENT", "shipped")


def test_list_all_orders_successfully(order_tracker, mock_storage):
    """Tests listing all current orders."""
    orders = {
        "ORD001": {
            "order_id": "ORD001",
            "item_name": "Laptop",
            "status": "pending"
        },
        "ORD002": {
            "order_id": "ORD002",
            "item_name": "Phone",
            "status": "shipped"
        }
    }
    mock_storage.get_all_orders.return_value = orders

    result = order_tracker.list_all_orders()
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(order["order_id"] in ["ORD001", "ORD002"] for order in result)
    mock_storage.get_all_orders.assert_called_once()


def test_list_orders_by_status_successfully(order_tracker, mock_storage):
    """Tests retrieving only orders with a specific status."""
    mock_storage.get_all_orders.return_value = {
        "ORD001": {
            "order_id": "ORD001",
            "item_name": "Laptop",
            "status": "pending"
        },
        "ORD002": {
            "order_id": "ORD002",
            "item_name": "Phone",
            "status": "shipped"
        },
        "ORD003": {
            "order_id": "ORD003",
            "item_name": "Tablet",
            "status": "pending"
        }
    }

    result = order_tracker.list_orders_by_status("pending")
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(order["status"] == "pending" for order in result)


def test_list_orders_by_status_returns_empty_if_none_found(
    order_tracker,
    mock_storage
):
    """Tests that filtering by non-existent status returns empty list."""
    mock_storage.get_all_orders.return_value = {
        "ORD001": {
            "order_id": "ORD001",
            "item_name": "Laptop",
            "status": "pending"
        },
        "ORD002": {
            "order_id": "ORD002",
            "item_name": "Phone",
            "status": "shipped"
        }
    }

    result = order_tracker.list_orders_by_status("cancelled")
    assert result == []
