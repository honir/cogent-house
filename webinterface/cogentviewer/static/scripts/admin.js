// Generated by CoffeeScript 1.6.3
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

require(["dojo/store/JsonRest", "dojo/store/Cache", "dojo/store/Observable", "dojo/store/Memory", "dgrid/OnDemandGrid", "dgrid/Keyboard", "dgrid/Selection", "dgrid/editor", "dgrid/extensions/DijitRegistry", "dojo/_base/declare", "MyWidgets/form/DateTimeBox", "dijit/form/FilteringSelect", "dojo/ready", "dojo/parser", "dijit/form/Button", "dijit/Dialog", "dojo/domReady!"], function(jsonRest, Cache, Observable, Memory, OnDemandGrid, Keyboard, Selection, editor, DijitRegistry, declare, DateTimeBox, FilteringSelect, ready, parser, Button, Dialog) {
  var baseGrid, deployGrid, deployNew, deployReset, deployStore, houseStore, roomStore, typeStore;
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
  console.log("Deployment Grid ", deployGrid);
  deployGrid.startup();
  parser.parse();
  deployReset = new Button({
    label: "Reset",
    onClick: function() {
      return deployGrid.revert();
    }
  }, "deployReset");
  deployReset.startup();
  deployNew = new Button({
    label: "Add",
    onClick: function() {
      return registry.byId("depDlg").show();
    }
  }, "deployNew");
  deployNew.startup();
});