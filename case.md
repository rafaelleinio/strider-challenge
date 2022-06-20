# Project Description

## **Overview**

It’s Tuesday morning and the product manager you work with comes to you with several files asking for help. The dataset contains information about a small startup streaming app in the month of December 2021. The company keeps data about its users, movies, and streaming activity. In order to answer some important questions about the product, external data was also acquired with information about books, authors, and reviews that can be linked to internal movies data.

### External data provided by the vendor

- authors.json: Famous authors’ information.
- books.json: Aggregated info about famous books.
- reviews.json: Reviews written by external vendors about movies that are based on books.

### Internal data

- users.csv: active users of the app.
- movies.csv: movies available in the app.
- streams.csv: historical streaming data from December 2021.

### Assumptions

- Two different authors don’t use the same name to publish books
- Two different books can’t be published using the exact same title
- Users can watch more than one movie at the time
- Users’ emails are verified and unique in the database

### Data download

[data.zip]()

[vendor.zip]()

## **Phase 1**

Due to unknown reasons, the vendor can delete and/or update existing records content (authors, books, and reviews data). Since we want to extract the best of the data we should retain historical records even if they got deleted on newly received dumps and avoid duplications in case of existing records updates.

Keeping that in mind, build an Extract, Transform, Load (ETL) pipeline that will take this data (and any newly received data) and move it into a **production-ready database** that can be easily and performant queried to answer questions for the business.

## **Phase 2**

Answer the following questions, and show the SQL queries you used to extract the data.

- What percentage of the streamed movies are based on books?
- During Christmas morning (7 am and 12 noon on December 25), a partial system outage was caused by a corrupted file. Knowing the file was part of the movie "Unforgiven" thus could affect any in-progress streaming session of that movie, how many users were potentially affected?
- How many movies based on books written by Singaporeans authors were streamed that month?
- What's the average streaming duration?
- What's the **median** streaming size in gigabytes?
- Given the stream duration (start and end time) and the movie duration, how many users watched at least 50% of any movie in the last week of the month (7 days)?

## **Phase 3**

In **as much detail as time provides**, describe how you would build this pipeline if you had more time for the test and planned to ship it in a production environment.

You should:

- Explain which technologies you would use (programming languages, frameworks, database, and pipeline) and **why** for each one
- Share a detailed architecture diagram
- Write down your reasoning process for the designed architecture, making sure you cover in detail the components and how they interact with each other.
- **Be thorough!**

Assumptions:

- You have about 8 GB of data coming every day
- Data needs to be moved through the pipeline and ready in the production database in less than one hour
- The vendor data is made available through File Transfer Protocol (FTP) and gets updated every night (2 am)
- Vendor data is always their whole dataset. Unfortunately, they can't publish updates only.
- The load process must be incremental given the vendor can delete data we want to retain