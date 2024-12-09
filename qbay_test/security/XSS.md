## XSS Security Report

|      | Route/URL                              |    Parameter     | XSS successful? |
| :--: | -------------------------------------- | :--------------: | :-------------: |
| Scan | http://127.0.0.1:8081/register         |      email       |       NO        |
| Scan | http://127.0.0.1:8081/register         |       name       |       NO        |
| Scan | http://127.0.0.1:8081/register         |     password     |       NO        |
| Scan | http://127.0.0.1:8081/register         |    password2     |       NO        |
| Scan | http://127.0.0.1:8081/register         |     register     |       NO        |
| Scan | http://127.0.0.1:8081/login            |      email       |       NO        |
| Scan | http://127.0.0.1:8081/login            |     password     |       NO        |
| Scan | http://127.0.0.1:8081/login            |    btn-submit    |       NO        |
| Scan | http://127.0.0.1:8081/product-creation |   product-name   |       NO        |
| Scan | http://127.0.0.1:8081/product-creation |   description    |       NO        |
| Scan | http://127.0.0.1:8081/product-creation |      price       |       NO        |
| Scan | http://127.0.0.1:8081/product-creation |     quantity     |       NO        |
| Scan | http://127.0.0.1:8081/product-creation |  submit-button   |       NO        |
| Scan | http://127.0.0.1:8081/update-profile   |       name       |       NO        |
| Scan | http://127.0.0.1:8081/update-profile   |  submit-button   |       NO        |
| Scan | http://127.0.0.1:8081/update-profile   | shipping-address |       NO        |
| Scan | http://127.0.0.1:8081/update-profile   |  submit-button   |       NO        |
| Scan | http://127.0.0.1:8081/update-profile   |   postal_code    |       NO        |
| Scan | http://127.0.0.1:8081/update-profile   |  submit-button   |       NO        |
| Scan | http://127.0.0.1:8081/update-profile   |     quantity     |       NO        |
| Scan | http://127.0.0.1:8081/logout           |       N/A        |       NO        |
| Scan | http://127.0.0.1:8081/                 |       N/A        |       NO        |

## Questions:

1. :ship: We did two rounds of scanning. Why the results are different? What is the purpose of adding in the session id?

The results are different because since we have gave the cookie in the second scan it can now access all pages of the website. In the first scan without the cookie passed, it could only access the following page extensions: "/, /login, /register". But with the cookie it can now access all the possible pages to be crawled of the website as it is considered to be a logged in session.

2. :ship: Are all the possible XSS (script injection) links/routes covered in the table above? (think about any links that will render user inputs, such as URL paramer, cookies, flask flash calls). If not, are those link/pages vulnerable to XSS?

No the "/update-product" page is never reached by the crawler. This is likely because this test account has not had a product created so there was no available link to the page so it couldn't crawl to it. This is the same reason "/shop" is never reached becayse the account being tested doesn't have any items created so it has no way to crawl to the shop page. As well, not all possible links have been tested as many of the links can have URL parameters and cookies values which can have an infinite number of combinations. But since the base links passed I would say with confidence that those link/pages are not vulnerable to XSS and are also safe as the base pages have no vulnerabilities.
