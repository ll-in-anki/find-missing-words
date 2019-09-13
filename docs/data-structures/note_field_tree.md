# Note Field Tree

Used in search to filter on notes and their fields.

The structure holds data useful for the QTreeWidget that represents this structure.

- State:
    - 0: Unchecked (`Qt.Unchecked`)
    - 1: Partially Checked (`Qt.PartiallyChecked`)
        - Only for note tree items
    - 2: Checked (`Qt.Checked`)
    - See [Qt documentation](https://doc.qt.io/qt-5/qt.html#CheckState-enum)

```json
[
    {
        name: "Note Name with No Fields Selected",
        state: 0,
        fields: [
            {
                name: "Field Name 1",
                state: 0
            },{
                name: "Field Name 2",
                state: 0
            }
        ]
    }, {
        name: "Note Name with Some Fields Selected",
        state: 1,
        fields: [
            {
                name: "Field Name 1",
                state: 2
            },{
                name: "Field Name 2",
                state: 0
            }
        ]
    }, {
        name: "Note Name with All Fields Selected",
        state: 2,
        fields: [
            {
                name: "Field Name 1",
                state: 2
            },{
                name: "Field Name 2",
                state: 2
            }
        ]
    }
]
```