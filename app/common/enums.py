from enum import Enum


class DrKleinRkDynamoDBTables(str, Enum):
    VORGAENGE = "drkleinrk-vorgaenge"
    VORGAENGE_STATUS = "drkleinrk-vorgaenge-status"
    ANTRAEGE = "drkleinrk-antraege"
    ANTRAGSTELLER = "drkleinrk-antragsteller"
    DOKUMENTE = "drkleinrk-dokumente"
    TIPPGEBER = "drkleinrk-tippgeber"
    VORGAENGE_MARTKPLATZ = "drkleinrk-vorgaenge-marktplatz"
    ANTRAEGE_MARTKPLATZ = "drkleinrk-antraege-marktplatz"
    FINANZIERUNGSVORSCHLAEGE_MARKTPLATZ = "drkleinrk-vorgaenge-marktplatz-finanzierungsvorschlaege"


class DataContext(Enum):
    PROD = "PROD"
    TEST = "TEST"
