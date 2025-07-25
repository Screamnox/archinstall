from typing import override

from archinstall.lib.menu.abstract_menu import AbstractSubMenu
from archinstall.lib.models.application import ApplicationConfiguration, BluetoothConfiguration
from archinstall.lib.translationhandler import tr
from archinstall.tui.curses_menu import SelectMenu
from archinstall.tui.menu_item import MenuItem, MenuItemGroup
from archinstall.tui.types import Alignment, Orientation


class ApplicationMenu(AbstractSubMenu[ApplicationConfiguration]):
	def __init__(
		self,
		preset: ApplicationConfiguration | None = None,
	):
		if preset:
			self._app_config = preset
		else:
			self._app_config = ApplicationConfiguration()

		menu_optioons = self._define_menu_options()
		self._item_group = MenuItemGroup(menu_optioons, checkmarks=True)

		super().__init__(
			self._item_group,
			config=self._app_config,
			allow_reset=True,
		)

	@override
	def run(self, additional_title: str | None = None) -> ApplicationConfiguration:
		super().run(additional_title=additional_title)
		return self._app_config

	def _define_menu_options(self) -> list[MenuItem]:
		return [
			MenuItem(
				text=tr('Bluetooth'),
				action=select_bluetooth,
				value=self._app_config.bluetooth_config,
				preview_action=self._prev_bluetooth,
				key='bluetooth_config',
			),
		]

	def _prev_bluetooth(self, item: MenuItem) -> str | None:
		if item.value is not None:
			bluetooth_config: BluetoothConfiguration = item.value

			output = 'Bluetooth: '
			output += tr('Enabled') if bluetooth_config.enabled else tr('Disabled')
			return output
		return None


def select_bluetooth(preset: BluetoothConfiguration | None) -> BluetoothConfiguration | None:
	group = MenuItemGroup.yes_no()
	group.focus_item = MenuItem.no()

	if preset is not None:
		group.set_selected_by_value(preset.enabled)

	header = tr('Would you like to configure Bluetooth?') + '\n'

	result = SelectMenu[bool](
		group,
		header=header,
		alignment=Alignment.CENTER,
		columns=2,
		orientation=Orientation.HORIZONTAL,
		allow_skip=True,
	).run()

	enabled = result.item() == MenuItem.yes()

	return BluetoothConfiguration(enabled)
