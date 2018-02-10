# cheqout
A project for QHacks 2018 by [Angelo Lu](https://github.com/angelolu/), [Zhijian Wang](https://github.com/EvW1998/), [Hayden Pfeiffer](https://github.com/PfeifferH/) and [Ian Wang](https://github.com/ianw3214/). Speeding up checkouts at supermarkets by fitting existing carts with tech enabling payments.
### Targeted Clients: Established supermarket chains
Big box supermarkets with established physical locations, large inventories and high traffic, such as Walmart and Loblaw-branded stores.
### Problems Identified: Slow checkouts
Checkout times can be slow because they are dependent on available checkout lanes and influenced by factors such as the number of items of the people in front of you and speed of the cashier and the person in scanning and paying. Stores with consistently slow checkouts are at risk of losing customers as people look for faster options such as other nearby stores or online shopping.
### Possible Solutions
1.  **Additional checkout lanes**
This solution is limited by the physical layout of the store. Additional checkout lanes require additional staff.
2.  **Self-checkout kiosks**
This solution is also limited by the physical layout. Lines can still develop as people must wait for others to scan and pay, which may take a long time.
3.  **Handheld self-scanners**
In supermarkets, products such as produce, and bulk foods are weighed, which cannot be processed easily with this solution.
4.  **Sensor-fusion based solution replacing checkouts (Ex. Amazon Go)**
In large chain supermarkets with many established locations, implementation of all the cameras, scales and custom shelving for the system requires massive renovations and is assumed to be impractical, especially considering the number of products and stores. 

### Proposed Solution: “cheqout”, Smart Shopping Carts
The solution, titled “cheqout” involves fitting existing shopping carts with a tray, covering the main basket of the cart, and a touchscreen and camera, on the cart handle. 
A customer would take out a cart upon entry and scan each items’ barcode before placing it in the cart. The touchscreen would display the current total of the cart in real time. Once the customer is ready to pay, they can simply tap “Check Out” on the touchscreen and scan a loyalty card (virtual or physical) with an associated payment method or tap their credit or debit card directly. Alternatively, the customer can proceed to a payment kiosk or traditional checkout if they do not have an account, are paying in cash or want a physical receipt, without having to wait for each item to be scanned again.
On the way out, there would be an employee with a handheld reader displaying what has been paid in the cart to do a quick visual inspection.
This solution trusts that most users will not steal products, however, a scale integrated in the tray will continuously monitor the weight of products in the cart and the changes in weight associated with an item’s addition/removal and prompt accordingly. The scale will also be used to weigh produce.
This solution allows for the sale of weighed and barcoded items while still decreasing checkout line congestion. It is scalable to meet the requirements of each individual store and does not require the hiring of many additional personnel.
### Challenges
*  Time: This project is being built for QHacks, a 36-hour hackathon
*  Technical: The scale and touch screen remain uncooperative, prompting temporary fixes for the purpose of the dem

### Possible Future Features/Value-Added Features
*  **Information about traffic within the store**
By implementing indoor location tracking, analysts can visualize where customers frequent and tailor/adjust product placement accordingly
*  **Information about product selection**
The system can record a customer’s decision making process and uncertainties based on how long they spend in one spot and if they add, remove or swap items from their cart
*  **Additional advertisement opportunities**
Current offers can be shown to the customer when they first take the cart or while they are shopping. This can be done through a offers button on the UI or automatically by integrating indoor location tracking.
