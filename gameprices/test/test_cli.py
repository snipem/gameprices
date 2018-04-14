from gameprices.cli.cli import eshop_main
from gameprices.shops.eshop import Eshop
import sys
import pytest

def test_cli_search():
    sys.argv = [
        "eshopcli",
        "--query",
        "'Vostok'"
    ]

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        eshop_main()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0

@pytest.mark.skip 
def test_cli_by_id_and_whish_price():
    sys.argv = [
        "eshopcli",
        "--id",
        "DE/de###1173281###Mario_Kart_8_Deluxe",
        "--price",
        "100"
    ]

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        eshop_main()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0