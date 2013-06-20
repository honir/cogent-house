// Generated by CoffeeScript 1.3.3
var dateFormatter;

require(["dojo/date", "dojo/date/locale"]);

dateFormatter = function(dateStr) {
  var fmtDate, theDate;
  console.log("Formatting Date ", dateStr);
  if (dateStr) {
    theDate = dojo.date.stamp.fromISOString(dateStr);
    fmtDate = dojo.date.locale.format(theDate, {
      format: "short"
    });
    return fmtDate;
  } else {
    return null;
  }
};

require(["dojo/store/JsonRest", "dojo/store/Cache", "dojo/store/Observable", "dojo/store/Memory", "dgrid/OnDemandGrid", "dgrid/Keyboard", "dgrid/Selection", "dgrid/editor", "dgrid/extensions/DijitRegistry", "dojo/_base/declare", "MyWidgets/form/DateTimeBox", "dijit/form/Button", "dijit/form/FilteringSelect", "dojo/ready", "dojo/on", "dijit/Dialog", "dijit/form/TextBox", "dijit/form/SimpleTextarea", "dojo/domReady!"], function(jsonRest, Cache, Observable, Memory, OnDemandGrid, Keyboard, Selection, editor, DijitRegistry, declare, DateTimeBox, Button, FilteringSelect, ready, On, Dialog, TextBox, SimpleTextarea) {
  var baseGrid, closeDlg, dep_cancel, dep_desc, dep_endDate, dep_name, dep_ok, dep_startDate, deployGrid, deployNew, deployReset, deploySave, deployStore, houseAdd, houseDelete, houseDep, houseEnd, houseGrid, houseNew, houseReset, houseSave, houseStart, houseStore, house_cancel, house_ok, procDep, procHouse, roomDelete, roomGrid, roomNew, roomReset, roomSave, roomStore, typeGrid, typeNew, typeReset, typeSave, typeStore;
  console.log("Starting Admin Interface");
  deployStore = Cache(Observable(jsonRest({
    target: "./rest/deployment/"
  })), Memory());
  houseStore = Cache(Observable(jsonRest({
    target: "./rest/house/"
  })), Memory());
  typeStore = Cache(Observable(jsonRest({
    target: "./rest/roomtype/"
  })), Memory());
  roomStore = Cache(Observable(jsonRest({
    target: "./rest/room/"
  })), Memory());
  baseGrid = new declare([OnDemandGrid, Keyboard, Selection, DijitRegistry]);
  deployGrid = baseGrid({
    columns: [
      {
        label: "Id",
        field: "id"
      }, editor({
        label: "Name",
        field: "name",
        editor: "text",
        dismissOnEnter: false,
        editOn: "click"
      }), editor({
        label: "Decription",
        field: "description",
        editor: "textarea",
        dismissOnEnter: false,
        editOn: "click"
      }), editor({
        label: "Start Date",
        field: "startDate",
        editor: DateTimeBox
      }), editor({
        label: "End Date",
        field: "endDate",
        editor: DateTimeBox
      })
    ],
    store: deployStore
  }, "deployGrid");
  houseGrid = baseGrid({
    columns: [
      {
        label: "Id",
        field: "id"
      }, editor({
        label: "Address",
        field: "address",
        editor: "text",
        editOn: "click"
      }), editor({
        label: "Deployment",
        field: "deploymentId",
        editor: FilteringSelect,
        editorArgs: {
          store: deployStore,
          style: "width:150px"
        }
      }), editor({
        label: "Start Date",
        field: "startDate",
        editor: DateTextBox
      }), editor({
        label: "End Date",
        field: "endDate",
        editor: DateTextBox
      })
    ],
    store: houseStore
  }, "houseGrid");
  roomGrid = baseGrid({
    columns: [
      {
        label: "Id",
        field: "id"
      }, editor({
        label: "Name",
        field: "name",
        editor: "text",
        editOn: "click"
      }), editor({
        label: "Type",
        field: "roomTypeId",
        editor: FilteringSelect,
        editorArgs: {
          store: typeStore
        }
      })
    ],
    store: roomStore
  }, "roomGrid");
  typeGrid = new declare([OnDemandGrid, Keyboard, Selection, DijitRegistry])({
    columns: [
      {
        label: "Id",
        field: "id"
      }, editor({
        label: "name",
        field: "name",
        editOn: "click"
      })
    ],
    store: typeStore
  }, "typeGrid");
  deployGrid.startup();
  houseGrid.startup();
  roomGrid.startup();
  typeGrid.startup();
  deploySave = new Button({
    label: "Save Changes",
    onClick: function() {
      return deployGrid.save();
    }
  }, "deploySave");
  deployReset = new Button({
    label: "Reset",
    onClick: function() {
      return deployGrid.revert();
    }
  }, "deployReset");
  deployNew = new Button({
    label: "Add",
    onClick: function() {
      return dijit.byId("depDlg").show();
    }
  }, "deployNew");
  deployReset = new Button({
    label: "Delete",
    onClick: function() {
      var id, selected;
      if (confirm("This Will Delete the Selected items")) {
        selected = deployGrid.selection;
        console.log("Selected ", selected);
        for (id in selected) {
          deployStore.remove(id);
        }
        return;
      }
    }
  }, "deployDelete");
  houseSave = new Button({
    label: "Save Changes",
    onClick: function() {
      return houseGrid.save();
    }
  }, "houseSave");
  houseReset = new Button({
    label: "Reset",
    onClick: function() {
      return houseGrid.revert();
    }
  }, "houseReset");
  houseNew = new Button({
    label: "Add",
    onClick: function() {
      return dijit.byId("houseDlg").show();
    }
  }, "houseNew");
  houseDelete = new Button({
    label: "Delete",
    onClick: function() {
      var id, selected;
      if (confirm("This Will Delete the Selected items")) {
        selected = houseGrid.selection;
        console.log("Selected ", selected);
        for (id in selected) {
          houseStore.remove(id);
        }
        return;
      }
    }
  }, "houseDelete");
  typeSave = new Button({
    label: "Save Changes",
    onClick: function() {
      return typeGrid.save();
    }
  }, "typeSave");
  typeReset = new Button({
    label: "Reset",
    onClick: function() {
      return typeGrid.revert();
    }
  }, "typeReset");
  typeNew = new Button({
    label: "Add",
    onClick: function() {
      return dijit.byId("typeDlg").show();
    }
  }, "typeNew");
  roomSave = new Button({
    label: "Save Changes",
    onClick: function() {
      return roomGrid.save();
    }
  }, "roomSave");
  roomReset = new Button({
    label: "Reset",
    onClick: function() {
      return roomGrid.revert();
    }
  }, "roomReset");
  roomNew = new Button({
    label: "Add",
    onClick: function() {
      return dijit.byId("roomDlg").show();
    }
  }, "roomNew");
  roomDelete = new Button({
    label: "Delete",
    onClick: function() {
      var id, selected;
      if (confirm("This Will Delete the Selected items")) {
        selected = roomGrid.selection;
        console.log("Selected ", selected);
        for (id in selected) {
          roomStore.remove(id);
        }
        return;
      }
    }
  }, "roomDelete");
  dep_name = new TextBox({
    required: true
  }, "dep_name");
  dep_name.startup();
  dep_desc = new SimpleTextarea({
    rows: 4,
    cols: 40
  }, "dep_desc");
  dep_desc.startup();
  dep_startDate = new DateTimeBox({}, "dep_startDate");
  dep_startDate.startup();
  dep_endDate = new DateTimeBox({}, "dep_endDate");
  dep_endDate.startup();
  dep_ok = new Button({
    label: "Save",
    onClick: function() {
      return procDep();
    }
  }, "dep_ok");
  dep_cancel = new Button({
    label: "Cancel",
    onClick: function() {
      return closeDlg("depDlg");
    }
  }, "dep_cancel");
  procDep = function() {
    var dlg, theItem, theStore;
    console.log("Processing");
    dlg = dijit.byId("depDlg");
    if (!dlg.validate()) {
      return;
    }
    theItem = {
      "__table__": "Deployment",
      name: dep_name.get("value"),
      description: dep_desc.get("value"),
      startDate: dep_startDate.get("value"),
      endDate: dep_endDate.get("value")
    };
    if (theItem.name === null) {
      return;
    }
    console.log(theItem);
    theStore = dijit.byId("deployGrid").store;
    theStore.add(theItem);
    return closeDlg("depDlg");
  };
  closeDlg = function(theName) {
    var dlg;
    dlg = dijit.byId(theName);
    dlg.reset();
    return dlg.hide();
  };
  houseAdd = new TextBox({
    required: true
  }, "house_add");
  houseAdd.startup();
  houseDep = new FilteringSelect({
    required: true,
    store: deployStore
  }, "house_dep");
  houseStart = new DateTimeBox({
    required: true
  }, "house_startDate");
  houseStart.startup();
  houseEnd = new DateTimeBox({}, "house_endDate");
  houseEnd.startup();
  house_ok = new Button({
    label: "Save",
    onClick: function() {
      return procHouse();
    }
  }, "house_ok");
  house_cancel = new Button({
    label: "Cancel",
    onClick: function() {
      return closeDlg("houseDlg");
    }
  }, "house_cancel");
  procHouse = function() {
    var dlg, item, theStore;
    console.log("Processing");
    dlg = dijit.byId("houseDlg");
    if (!dlg.validate()) {
      return;
    }
    item = {
      "table": "__house__",
      address: houseAdd.get("value"),
      deploymentId: houseDep.get("value"),
      startDate: houseStart.get("value"),
      endDate: houseEnd.get("value")
    };
    console.log(item);
    theStore = dijit.byId("houseGrid").store;
    theStore.add(item);
    return closeDlg("houseDlg");
  };
});
