import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from ..util import (
    get_youngest_search,
    fetch_db_prices_search,
    save_search_data,
    get_prices,
)
from ..models import Search as SearchModel


def test_get_youngest_search_valid_input(mocker):
    # Mock the database session and query
    mock_session = mocker.MagicMock()
    mocker.patch("backend.util.db.session", mock_session)
    mock_query = (
        mock_session.query.return_value.filter.return_value.order_by.return_value
    )
    mock_query.first.return_value = SearchModel(
        Term="apple", ZipCode="90001", LastModified=datetime.now()
    )

    result = get_youngest_search("apple", "90001")
    assert result.term == "apple"
    assert result.zip_code == "90001"


def test_get_youngest_search_invalid_input(mocker):
    # Mock the database session and query
    mock_session = mocker.MagicMock()
    mocker.patch("backend.util.db.session", mock_session)
    mock_query = (
        mock_session.query.return_value.filter.return_value.order_by.return_value
    )
    mock_query.first.return_value = None

    result = get_youngest_search("invalidItem", "12345")
    assert result is None


def test_fetch_db_prices_search_valid_search(mocker):
    mock_session = mocker.MagicMock()
    mocker.patch("backend.util.db.session", mock_session)
    mock_query = mock_session.query.return_value.filter.return_value
    mock_store_price = MagicMock()
    mock_store_price.store = MagicMock(Name="TestStore")
    mock_store_price.product = MagicMock(Name="TestProduct")
    mock_store_price.Price = 5.0
    mock_query.all.return_value = [mock_store_price]

    search = MagicMock(id=1)  # Mocked SearchDomain object with id=1
    prices = fetch_db_prices_search(search)
    assert prices[0]["price"] == 5.0


def test_fetch_db_prices_search_invalid_search(mocker):
    mock_session = mocker.MagicMock()
    mocker.patch("backend.util.db.session", mock_session)
    mock_query = mock_session.query.return_value.filter.return_value
    mock_query.all.return_value = []

    search = MagicMock(id=1)  # Mocked SearchDomain object with id=1
    prices = fetch_db_prices_search(search)
    assert prices is None


def test_save_search_data_new_search(mocker):
    # Mocking session and related methods
    mock_session = mocker.MagicMock()
    mocker.patch("backend.util.db.session", mock_session)

    mock_query = mock_session.query.return_value
    mock_filter_by = mock_query.filter_by.return_value
    mock_filter_by.first.return_value = (
        None  # Simulate that the object doesn't exist in the DB
    )

    # Mock flush and commit methods
    mock_session.flush.return_value = None
    mock_session.commit.return_value = None

    # Mocking SearchDomain.from_orm
    mock_from_orm = mocker.patch(
        "backend.util.SearchDomain.from_orm", return_value=MagicMock(term="apple")
    )

    # Mocked SearchDomain object without id
    search = MagicMock(id=None)
    data = [
        {
            "store": {
                "name": "TestStore",
                "api_reference": "ref",
                "chain": "chain",
                "zip_code": "12345",
                "address": "address",
            },
            "product": {"name": "TestProduct", "UPC": "123456", "price": 5.0},
        }
    ]

    result = save_search_data(search, data)

    # Check if the SearchDomain.from_orm mock was called
    mock_from_orm.assert_called_once()


def test_save_search_data_existing_search(mocker):
    # Mocking session and related methods
    mock_session = mocker.MagicMock()
    mocker.patch("backend.util.db.session", mock_session)
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = (
        MagicMock()
    )  # Simulate that the object exists in the DB
    mock_session.flush.return_value = None
    mock_session.commit.return_value = None

    # Mocking SearchDomain.from_orm
    mocker.patch(
        "backend.util.SearchDomain.from_orm", return_value=MagicMock(term="apple")
    )

    # Mocked SearchDomain object with id=1
    search = MagicMock(id=1)
    data = [
        {
            "store": {
                "name": "TestStore",
                "api_reference": "ref",
                "chain": "chain",
                "zip_code": "12345",
                "address": "address",
            },
            "product": {"name": "TestProduct", "UPC": "123456", "price": 5.0},
        }
    ]

    result = save_search_data(search, data)
    assert result.term == "apple"


def test_save_search_data_db_exception(mocker):
    mock_session = mocker.MagicMock()
    mocker.patch("backend.util.db.session", mock_session)
    mock_session.add.side_effect = Exception("Database Error")

    search = MagicMock(id=None)  # Mocked SearchDomain object without id
    data = [
        {
            "store": {"name": "TestStore"},
            "product": {"name": "TestProduct", "UPC": "123456"},
            "price": 5.0,
        }
    ]
    result = save_search_data(search, data)
    assert result is None


def test_get_prices_fresh_search(mocker):
    mocker.patch(
        "backend.util.get_youngest_search",
        return_value=MagicMock(updated_at=datetime.now()),
    )
    mocker.patch("backend.util.fetch_db_prices_search", return_value=[{"price": 5.0}])

    prices = get_prices("apple", "90001")
    assert prices[0]["price"] == 5.0


def test_get_prices_stale_search(mocker):
    mocker.patch(
        "backend.util.get_youngest_search",
        return_value=MagicMock(updated_at=datetime.now() - timedelta(days=2)),
    )
    mocker.patch(
        "backend.util.fetch_best_prices",
        return_value=[
            {
                "store": {"name": "TestStore"},
                "product": {"name": "TestProduct", "UPC": "123456"},
                "price": 5.0,
            }
        ],
    )
    mocker.patch("backend.util.save_search_data")
    mocker.patch("backend.util.fetch_db_prices_search", return_value=[{"price": 5.0}])

    prices = get_prices("apple", "90001")
    assert prices[0]["price"] == 5.0


def test_get_prices_db_exception(mocker):
    mocker.patch(
        "backend.util.get_youngest_search", side_effect=Exception("Database Error")
    )

    prices = get_prices("apple", "90001")
    assert len(prices) == 0
