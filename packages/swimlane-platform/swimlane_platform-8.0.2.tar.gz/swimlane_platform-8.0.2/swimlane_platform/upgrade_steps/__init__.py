from typing import List, Type
from swimlane_platform.upgrade_steps.upgrade_step import UpgradeStep
from swimlane_platform.upgrade_steps.upgrade_from_700_701 import UpgradeFrom700To701
from swimlane_platform.upgrade_steps.upgrade_from_701_800 import UpgradeFrom701To800
from swimlane_platform.upgrade_steps.upgrade_from_800_801 import UpgradeFrom800To801

Upgrades = [UpgradeFrom700To701, UpgradeFrom701To800, UpgradeFrom800To801]  # type: List[Type[UpgradeStep]]
