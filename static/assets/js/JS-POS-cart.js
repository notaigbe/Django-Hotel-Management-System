var cart = {
  // (A) PROPERTIES
  items : {}, // current items in cart

  // (B) SAVE CURRENT CART INTO LOCALSTORAGE
  save : () => localStorage.setItem("cart", JSON.stringify(cart.items)),

  // (C) LOAD CART FROM LOCALSTORAGE
  load : () => {
    cart.items = localStorage.getItem("cart");
    if (cart.items == null) { cart.items = {}; }
    else { cart.items = JSON.parse(cart.items); }
  },

  // (D) NUKE CART!
  nuke : () => {
    cart.items = {};
    localStorage.removeItem("cart");
    cart.list();
  },

  // (E) INITIALIZE - RESTORE PREVIOUS SESSION
  init : () => {
    cart.load();
    cart.list();
  },

  // (F) LIST CURRENT CART ITEMS (IN HTML)
  list : () => {
    // (F1) DRAW CART INIT
    var wrapper = document.getElementById("poscart"),
        item, part, pdt,
        total = 0, subtotal = 0,
        empty = true;
    wrapper.innerHTML = "";
    for (let key in cart.items) {
      if (cart.items.hasOwnProperty(key)) { empty = false; break; }
    }

    // (F2) CART IS EMPTY
    if (empty) {
      item = document.createElement("div");
      item.innerHTML = "Cart is empty";
      wrapper.appendChild(item);
    }

    // (F3) CART IS NOT EMPTY - LIST ITEMS
    else {
      for (let pid in cart.items) {
        // CURRENT ITEM
        pdt = products.list[pid];
        item = document.createElement("div");
        item.className = "citem";
        wrapper.appendChild(item);

        // ITEM NAME
        part = document.createElement("span");
        part.innerHTML = pdt.name;
        part.className = "cname";
        item.appendChild(part);

        // REMOVE
        part = document.createElement("input");
        part.type = "button";
        part.value = "X";
        part.className = "cdel";
        part.onclick = () => cart.remove(pid);
        item.appendChild(part);

        // QUANTITY
        part = document.createElement("input");
        part.type = "number";
        part.min = 0;
        part.value = cart.items[pid];
        part.className = "cqty";
        part.onchange = function () { cart.change(pid, this.value); };
        item.appendChild(part);

        // SUBTOTAL
        subtotal = cart.items[pid] * pdt.price;
        total += subtotal;
      }

      // TOTAL AMOUNT
      item = document.createElement("div");
      item.className = "ctotal";
      item.id = "ctotal";
      item.innerHTML ="TOTAL: $" + total;
      wrapper.appendChild(item);

      // EMPTY BUTTON
      item = document.createElement("input");
      item.type = "button";
      item.value = "Empty";
      item.onclick = cart.nuke;
      item.id = "cempty";
      wrapper.appendChild(item);

      // CHECKOUT BUTTON
      item = document.createElement("input");
      item.type = "button";
      item.value = "Checkout";
      item.onclick = cart.checkout;
      item.id = "ccheckout";
      wrapper.appendChild(item);
    }
  },

  // (G) ADD ITEM TO CART
  add : pid => {
    if (cart.items[pid] == undefined) { cart.items[pid] = 1; }
    else { cart.items[pid]++; }
    cart.save(); cart.list();
  },

  // (H) CHANGE QUANTITY
  change : (pid, qty) => {
    // (H1) REMOVE ITEM
    if (qty <= 0) {
      delete cart.items[pid];
      cart.save(); cart.list();
    }

    // (H2) UPDATE TOTAL ONLY
    else {
      cart.items[pid] = qty;
      var total = 0;
      for (let id in cart.items) {
        total += cart.items[pid] * products.list[pid].price;
        document.getElementById("ctotal").innerHTML ="TOTAL: $" + total;
      }
    }
  },

  // (I) REMOVE ITEM FROM CART
  remove : pid => {
    delete cart.items[pid];
    cart.save(); cart.list();
  },

  // (J) CHECKOUT
  checkout : () => {
    orders.print();
    orders.add();
  }
};
window.addEventListener("DOMContentLoaded", cart.init);