var products = {
  // (A) PRODUCTS LIST
  list : {
    1 : { name:"Banana", img:"banana.png", price: 12 },
    2 : { name:"Cherry", img:"cherry.png", price: 23 },
    3 : { name:"Ice Cream", img:"icecream.png", price: 54 },
    4 : { name:"Orange", img:"orange.png", price: 65 },
    5 : { name:"Strawberry", img:"strawberry.png", price: 34 },
    6 : { name:"Watermelon", img:"watermelon.png", price: 67 }
  },

  // (B) DRAW HTML PRODUCTS LIST
  draw : () => {
    // (B1) TARGET WRAPPER
    const wrapper = document.getElementById("poslist");

    // (B2) CREATE PRODUCT HTML
    for (let pid in products.list) {
      // CURRENT PRODUCT
      let p = products.list[pid],
          pdt = document.createElement("div"),
          segment;

      // PRODUCT SEGMENT
      pdt.className = "pwrap";
      pdt.onclick = () => cart.add(pid);
      wrapper.appendChild(pdt);

      // IMAGE
      segment = document.createElement("img");
      segment.className = "pimg";
      segment.src = "images/" + p.img;
      pdt.appendChild(segment);

      // NAME
      segment = document.createElement("div");
      segment.className = "pname";
      segment.innerHTML = p.name;
      pdt.appendChild(segment);

      // PRICE
      segment = document.createElement("div");
      segment.className = "pprice";
      segment.innerHTML = "$" + p.price;
      pdt.appendChild(segment);
    }
  }
};
window.addEventListener("DOMContentLoaded", products.draw);