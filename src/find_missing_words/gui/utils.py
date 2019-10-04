def clear_layout(layout):
    for i in reversed(range(layout.count())):
        widget = layout.itemAt(i).widget()
        layout.removeWidget(widget)
        widget.deleteLater()


def clear_stacked_widget(stacked_widget):
    for i in reversed(range(stacked_widget.count())):
        widget = stacked_widget.widget(i)
        if widget:
            stacked_widget.removeWidget(widget)
            widget.deleteLater()
