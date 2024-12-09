## SQL Injection Testing

Listed below are the results of using SQLmap to probe our website for security vulnerabilities (specifically, SQL injection vulnerabilities).

**SQL Injection Testing Results:**
\_ | Route/URL | Parameter | Number of Injection Trials | Number of Successful Trials
-|-----------|-----------|----------------------------|----------------------------
Scan | http://127.0.0.1:8081/ | email | 14 | 0
Scan | http://127.0.0.1:8081/ | password | 14 | 0
Scan | http://127.0.0.1:8081/product-creation | product-name | 14 | 0
Scan | http://127.0.0.1:8081/product-creation | description | 14 | 0
Scan | http://127.0.0.1:8081/product-creation | price | 14 | 0
Scan | http://127.0.0.1:8081/product-creation | quantity | 14 | 0
Scan | http://127.0.0.1:8081/update-profile | name | 14 | 0
Scan | http://127.0.0.1:8081/update-profile | submit-button | 14 | 0
Scan | http://127.0.0.1:8081/update-profile | shipping_address | 14 | 0
Scan | http://127.0.0.1:8081/update-profile | postal_code | 14 | 0
Scan | http://127.0.0.1:8081/update-product?pin=&btn=Confirm Pin | pin | 14 | 0
Scan | http://127.0.0.1:8081/update-product?pin=&btn=Confirm Pin | btn | 14 | 0
Scan | http://127.0.0.1:8081/register | email | 14 | 0
Scan | http://127.0.0.1:8081/register | name | 14 | 0
Scan | http://127.0.0.1:8081/register | password | 14 | 0
Scan | http://127.0.0.1:8081/register | password2 | 14 | 0
Scan | http://127.0.0.1:8081/login | email | 14 | 0
Scan | http://127.0.0.1:8081/login | password | 14 | 0
Scan | http://127.0.0.1:8081/update-product?\_\_debugger\_\_=yes&cmd=resource&f=console.png | \_\_debugger\_\_ | 14 | 0
Scan | http://127.0.0.1:8081/update-product?\_\_debugger\_\_=yes&cmd=resource&f=console.png | cmd | 14 | 0
Scan | http://127.0.0.1:8081/update-product?\_\_debugger\_\_=yes&cmd=resource&f=console.png | f | 14 | 0
Scan | http://127.0.0.1:8081/shop | product_title | 14 | 0
Scan | http://127.0.0.1:8081/shop | App (the name of a test product) | 14 | 0

**Questions & Answers:**

1. 🚢 Are all the user input fileds in your application covered in all the test cases above? Any successful exploit?

All the user input fields in our application are covered by the test cases (there are no successful exploits). The only user input fields not tested in the testing coverage listed above are the "update-product" input forms. As this page requires a product to exist to reach, the automated testing did not find (or at least could not utilise) the input forms on this page.

2. 🚢 We did two rounds of scanning. Why the results are different? What is the purpose of adding in the session id?

By adding in the session id, the SQLmap software can now access pages that require authentication. Since all pages (except the login and register page) require a user to have logged in already, the SQLmap software cannot access the forms on most pages. By providing the session id (cookie), the SQLmap software can pretend to be the already logged in user and gain access to restricted pages. With access to these new pages, SQLmap can attempt an SQL injection on all of the newly accessable forms.

3. 🚢 Summarize the injection payload used based on the logs, and breifly discuss the purpose.

Based on the logs generated, a number of different injection payloads were attempted on each input form. Most of the tests completed tested specific vulnerabilities only present in certain SQL databases (e.g. using MySQL, PostgreSQL, Microsoft SQL Server, etc.). As each type of SQL database has its own unique traits (and vulnerabilities), they can be infiltrated using different techniques. With this in mind, it is incredibly important to use whichever software or libraries you choose _effectively_. Some services provide unnecessary features by default which could provide extra vulnerabilities, while other services are inherently less secure. All of these factors must be considered when choosing a service, language, framework, other tool. In addition to these tests, some injection payloads were attempted without any specific SQL database in mind (e.g. AND boolean-based blind). All of these tests help to show potential vulnerabilities in the system, espcially from using a specific type of SQL server. Moreover, some of the tests targeted security vulnerabilities that only exist on certain versions of the SQL server, further emphasizing the importance of updating your dependencies and other software when working on a project.
