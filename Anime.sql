/*==============================================================*/
/* DBMS name:      Sybase SQL Anywhere 12                       */
/* Created on:     2018-8-1 23:58:31                            */
/*==============================================================*/


drop table if exists AnimeInfo;

drop table if exists AnimeMX;

/*==============================================================*/
/* Table: AnimeInfo                                             */
/*==============================================================*/
create table AnimeInfo 
(
   animeName            varchar(50)                    not null,
   animeTime            date                           null,
   animeCountry         varchar(50)                    null,
   IsEnd                bit                            null,
   Episodes             int                            null,
   playCount            int                            null,
   fansCount            int                            null,
   coinCount            int                            null,
   danmuCount           int                            null,
   tags                 varchar(50)                    null,
   introText            varchar(500)                   null,
   score                varchar(5)                     null,
   VA                   varchar(500)                   null,
   STAFF                varchar(500)                   null,
   constraint PK_ANIMEINFO primary key clustered (animeName)
);

comment on table AnimeInfo is 
'保存番剧的所有基本信息';

/*==============================================================*/
/* Table: AnimeMX                                               */
/*==============================================================*/
create table AnimeMX 
(
   animeName            varchar(50)                    not null,
   EpisodeName          varchar(50)                    null,
   avSec                varchar(50)                    null,
   play                 int                            null,
   danmu                int                            null,
   coin                 int                            null,
   constraint PK_ANIMEMX primary key clustered (animeName)
);

