import pytest

from gameprices.cli.mailalert import main as psnmailalert_main
from gameprices.test.commons import mailalert
from gameprices.test.test_psn import NO_SEARCH_FOR_CID_REASON


def test_mailfunc_not_existing():
    wrong_line = "EP9000-CUSA07123_00-000000000000000,10.00,DE/de"
    mailalert(wrong_line, psnmailalert_main, should_remain_in_file=wrong_line)


@pytest.mark.skip(reason=NO_SEARCH_FOR_CID_REASON)
def test_mailfunc_existing_and_not_existing():
    unmatchable_price = "EP9000-CUSA07123_00-NIOHEU0000000000,0.00,DE/de"
    matchable_and_unmatchable_price = (
        unmatchable_price + "\nEP9000-CUSA07123_00-NIOHEU0000000000,100.00,DE/de"
    )
    mailalert(
        matchable_and_unmatchable_price,
        psnmailalert_main,
        should_remain_in_file=unmatchable_price + "\n",
    )



@pytest.mark.skip(reason=NO_SEARCH_FOR_CID_REASON)
def test_support_lines_without_store():
    mailalert("EP0177-CUSA07010_00-SONICMANIA000000,100.00", psnmailalert_main)
