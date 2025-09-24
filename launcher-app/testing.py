// ...existing code...
    def slot_data_button_checked(self):
        get_list_data_button = self.sender().property("button_data")
        print(f"emit from slot_data_button_checked= {get_list_data_button}")
        self.list_transfer.emit(get_list_data_button)

        for button in self.button_group.buttons():
            if button.isChecked():
                print(f"Button {button.text()} is checked")

    def get_signal_from_search(self, text_search):
        # 1. Determine which buttons should be visible
        visible_buttons = []
        for button in self.button_group.buttons():
            button_text = button.text()
            # Hide all buttons initially. They will be re-added if they match.
            button.hide() 
            if text_search.strip() == "" or re.search(text_search.lower(), button_text.lower()):
                visible_buttons.append(button)

        # 2. Remove all widgets from the grid layout
        self.cleanup_button()

        # 3. Re-add only the visible buttons to the grid
        positions = self.get_grid_coordinate()
        for position, button in zip(positions, visible_buttons):
            button.show()
            self.grid.addWidget(button, *position, alignment=(QtCore.Qt.AlignmentFlag.AlignTop |
                                                               QtCore.Qt.AlignmentFlag.AlignLeft))
// ...existing code...