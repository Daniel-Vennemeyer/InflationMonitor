# InflationMonitor

## Description of Project

###
We are using a custom Nostr relay to collect pricing data for common goods. Nostr is a simple, open protocol that enables a truly censorship-resistant and global 
social network. Consumers enter the pricing data in a certain format that specifies the item, cost, and location for more hyperlocal data. This is stored in a 
SQLite database. We extract this data from the SQLite Database using a Python API and then move it to ComposeDB on Ceramic using Python Requests for GraphQL Queries. 
ComposeDB on Ceramic is a decentralized, composable graph database. We wanted to use a Web3 native database that also provided the ability to sign in with Web3 wallets 
(coming soon) and help us in discovering inflation trends and relationships as we keep collecting more data.
