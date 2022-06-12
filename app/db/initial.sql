create table if not exists users
(
	id serial primary key,
	login text not null unique,
	hashed_password text not null,
	name text not null,
	surname text not null,
	date_of_birth timestamp not null,
	email text not null,
	phone text not null
);
create table if not exists teams
(
	id serial primary key,
	name text not null unique
);
create table if not exists tags
(
	id serial primary key,
	name text not null unique
);
create table if not exists companies
(
	id serial primary key,
	name text not null unique
);
create table if not exists tasks
(
	id serial primary key,
	name text not null,
	description text,
	task_type text,
	image_url text,
	company_id integer references companies(id) on delete set null,
	owner_id integer references users(id) on delete set null,
	start_date timestamp,
	end_date timestamp
);
create table if not exists tags_tasks
(
	id serial primary key,
	tag_id integer references tags(id) on delete cascade,
	task_id integer references tasks(id) on delete cascade,
	unique(tag_id, task_id)
);
create table if not exists teams_tasks
(
	id serial primary key,
	team_id integer references teams(id) on delete cascade,
	task_id integer references tasks(id) on delete cascade,
	completed boolean,
	unique(team_id, task_id)
);
create table if not exists users_tasks
(
	id serial primary key,
	user_id integer references users(id) on delete cascade,
	task_id integer references tasks(id) on delete cascade,
	completed boolean,
	unique(user_id, task_id)
);
create table if not exists users_teams
(
	id serial primary key,
	user_id integer references users(id) on delete cascade,
	team_id integer references teams(id) on delete cascade,
	unique(user_id, team_id)
);
create table if not exists companies
(
	id serial primary key,
	name text not null unique
);
create table if not exists skills
(
	id serial primary key,
	name text unique
);
create table if not exists users_skills
(
	id serial primary key,
	skill_id integer references skills(id) on delete cascade,
	user_id integer references users(id) on delete cascade,
	unique(skill_id,user_id)
);
create table if not exists favourites
(
	id serial primary key,
	owner_id integer references users(id) on delete cascade,
	fav_id integer references users(id) on delete cascade,
	unique(owner_id,fav_id)	
);
create table if not exists products
(
	id serial primary key,
	name text not null,
	description text,
	image_url text,
	price integer	
);
create table if not exists users_products
(
	id serial primary key,
	user_id integer references users(id),
	product_id integer references products(id)	
);
create table if not exists teams_products
(
	id serial primary key,
	team_id integer references teams(id),
	product_id integer references products(id)	
);
