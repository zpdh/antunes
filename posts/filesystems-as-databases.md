---
title: filesystems as databases
date: 2026-09-28
---

# Filesystems as databases

I recently started working on an older project with a data setup I wasn't used to. It made me rethink what a database is or has to be.

## Layers of data

This project has a few layers or data:

1. Redis: It's the central database, and also where the app reads and writes things on the go, while it's happening. The "hot" data layer. It's also serves as the store for a lot of data.
2. JSON files on a NFS: This is where a lot of data ends up; Redis gets exported periodically to .json files, and other services consume them. There's also some pure config and persistent storage data, unrelated to Redis.
3. files on a NFS: This is some of the more interesting and stuff I got to work with. A lot of data lives on Redis and gets exported periodically to .json files. It serves as multiple types of data stores, ranging from anywhere between an actual filesystem to an IPC bus. It's quite a new experience for me.
4. SQL: There's also a SQL database, although it's not a main or center-piece data store. It goes untouched by most of the production code; It's writes come from third-party logging and analytics services.

The main surprise for me was the NFS. This is where some of the more interesting stuff happens:

- It serves as a Filesystem in the ordinary sense. Data sits there, used by the applications mounted on it.
- There's lots of static data that sits there, never changing at runtime. They just get read.
- It also serves as some sort of IPC bus. A process writes a file, another one consumes it.

It's very peculiar. I never really thought about a shared directory as a way for programs to communicate with eachother for real production systems, but it just works. I find it very clever. There's no need for a message broker, server/client library, no connection to manage. If a process has access to it, it can take part.

Some of the things to consider about this approach:

- It's very easy to work with and debug. You can, quite literally, just look at the data.
- Sharing and integration is very simple. Anyone who can mount on the directory can consume it's data. This also means ownership is not very strictly defined. This is both an upside or and a downside, depending on the situation.
- Data can be stale. It's not constantly updated everytime there's an update on an entry. The data is written on a snapshot basis; It's not real time data, it's data from the last export.
- No specific querying. There's no indexes, no joins, no nothing. If you want to filter the data, you either keep a separate index for it or you load all of it's data and perform operations on top of it.

There's probably a lot of bullet points I've missed, but this has certainly shaped my view on data. Sometimes the question may not be "what is the best database for this problem?" but "what does this data need?".

Maybe it just needs to be fast. Redis is a good pick for this. Maybe permissions isn't deemed an issue, and you just need periodic reads/writes, no need for concurrency, complicated schemas or migrations. In this case, maybe writing to a shared folder is a good idea. It's cheap and provides exactly what you need.

It's a very different way of building and interpreting data from the way I was used to. I love these little things about software engineering. Seeing a problem being solved in completely different ways and figuring out the reasoning behind it.

---
