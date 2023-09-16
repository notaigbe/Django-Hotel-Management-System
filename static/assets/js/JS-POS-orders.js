var orders = {
  // (A) PROPERTIES
  iName : "JSPOS",
  iDB : null, iOrders : null, iItems : null,

  // (B) INIT
  init : () => {
    // (B1) REQUIREMENTS CHECK - INDEXED DB
    window.indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB;
    if (!window.indexedDB) {
      alert("Your browser does not support indexed database.");
      return;
    }

    // (B2) OPEN IDB
    let req = window.indexedDB.open(orders.iName, 1);

    // (B3) IDB OPEN ERROR
    req.onerror = evt => {
      alert("Indexed DB init error - " + evt.message);
      console.error(evt);
    };

    // (B4) IDB UPGRADE NEEDED
    req.onupgradeneeded = evt => {
      orders.iDB = evt.target.result;

      // (B4-1) IDB UPGRADE ERROR
      orders.iDB.onerror = evt => {
        alert("Indexed DB upgrade error - " + evt.message);
        console.error(evt);
      };

      // (B4-2) IDB VERSION 1
      if (evt.oldVersion < 1) {
        // ORDERS STORE
        let store = orders.iDB.createObjectStore("Orders", {
          keyPath: "oid",
          autoIncrement: true
        });
        store.createIndex("time", "time");

        // ORDER ITEMS STORE
        store = orders.iDB.createObjectStore("Items", {
          keyPath: ["oid", "pid"]
        });
        store.createIndex("qty", "qty");
      }
    };

    // (B6) IDB OPEN OK
    req.onsuccess = evt => {
      orders.iDB = evt.target.result;
      orders.iOrders = () => {
        return orders.iDB
        .transaction("Orders", "readwrite")
        .objectStore("Orders");
      };
      orders.iItems = () => {
        return orders.iDB
        .transaction("Items", "readwrite")
        .objectStore("Items");
      };
    };
  },

  // (C) ADD NEW ORDER
  add : () => {
    // (C1) INSERT ORDERS STORE
    let req = orders.iOrders().put({ time: Date.now() });

    // (C2) THE PAINFUL PART - INDEXED DB IS ASYNC
    // HAVE TO WAIT UNTIL ALL IS ADDED TO DB BEFORE CLEAR CART
    // THIS IS TO TRACK THE NUMBER OF ITEMS ADDED TO DATABASE
    let size = 0, entry;
    for (entry in cart.items) {
      if (cart.items.hasOwnProperty(entry)) { size++; }
    }
    
    // (C3) INSERT ITEMS STORE
    entry = 0;
    req.onsuccess = e => {
      oid = req.result;
      for (let pid in cart.items) {
        req = orders.iItems().put({ oid: oid, pid: pid, qty: cart.items[pid] });
        req.onsuccess = () => {
          entry++;
          if (entry == size) { cart.nuke(); }
        };
      }
    };
  },

  // (D) PRINT RECEIPT FOR CURRENT ORDER
  print : () => {
    // (D1) GENERATE RECEIPT
    var wrapper = document.getElementById("posreceipt");
    wrapper.innerHTML = "";
    for (let pid in cart.items) {
      let item = document.createElement("div");
      item.innerHTML = `${cart.items[pid]} X ${products.list[pid].name}`;
      wrapper.appendChild(item);
    }

    // (D2) PRINT
    var printwin = window.open();
    printwin.document.write(wrapper.innerHTML);
    printwin.stop();
    printwin.print();
    printwin.close();
  }
};
window.addEventListener("DOMContentLoaded", orders.init);