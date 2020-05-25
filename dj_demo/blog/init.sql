BEGIN;
--
-- Create model Category
--
CREATE TABLE "blog_category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(20) NOT NULL);
--
-- Create model Menu
--
CREATE TABLE "blog_menu" ("rank" integer NOT NULL UNIQUE, "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(20) NOT NULL, "method" varchar(20) NOT NULL);
--
-- Create model Tag
--
CREATE TABLE "blog_tag" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(20) NOT NULL);
--
-- Create model Author
--
CREATE TABLE "blog_author" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "phone" varchar(20) NOT NULL, "mod_time" datetime NOT NULL, "author_name_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEF
ERRED);
--
-- Create model Article
--
CREATE TABLE "blog_article" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL, "sub_title" varchar(140) NOT NULL, "overview" varchar(200) NOT NULL, "text" text NOT NULL, "create_time" datetime NOT NULL,
 "modity_time" datetime NOT NULL, "author_id" integer NOT NULL REFERENCES "blog_author" ("id") DEFERRABLE INITIALLY DEFERRED, "category_id" integer NOT NULL REFERENCES "blog_category" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "blog_article_tag" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "article_id" integer NOT NULL REFERENCES "blog_article" ("id") DEFERRABLE INITIALLY DEFERRED, "tag_id" integer NOT NULL REFERENCES "blog_tag" ("id") D
EFERRABLE INITIALLY DEFERRED);
CREATE INDEX "blog_article_author_id_905add38" ON "blog_article" ("author_id");
CREATE INDEX "blog_article_category_id_7e38f15e" ON "blog_article" ("category_id");
CREATE UNIQUE INDEX "blog_article_tag_article_id_tag_id_818e752b_uniq" ON "blog_article_tag" ("article_id", "tag_id");
CREATE INDEX "blog_article_tag_article_id_8db2395e" ON "blog_article_tag" ("article_id");
CREATE INDEX "blog_article_tag_tag_id_f2afe66b" ON "blog_article_tag" ("tag_id");
COMMIT;
