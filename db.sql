BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "confidencechronograms_material" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"nome"	varchar(200) NOT NULL,
	"unidade"	varchar(20) NOT NULL,
	"valor_unitario"	decimal NOT NULL,
	"quantidade"	decimal NOT NULL,
	"categoria_id"	integer NOT NULL,
	"cronograma_id"	integer NOT NULL,
	"deposito_id"	integer NOT NULL,
	"date_added"	datetime NOT NULL,
	"date_update"	datetime NOT NULL,
	FOREIGN KEY("deposito_id") REFERENCES "confidencechronograms_deposito"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("cronograma_id") REFERENCES "confidencechronograms_cronograma"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("categoria_id") REFERENCES "confidencechronograms_categoria"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
CREATE TABLE IF NOT EXISTS "confidencechronograms_comentario" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"nome_cliente"	varchar(60) NOT NULL,
	"assunto"	varchar(60) NOT NULL,
	"descricao"	text NOT NULL,
	"arquivo"	varchar(100),
	"date_added"	datetime NOT NULL,
	"date_update"	datetime NOT NULL,
	"cliente_id"	integer NOT NULL,
	"funcionario_id"	integer NOT NULL,
	FOREIGN KEY("cliente_id") REFERENCES "confidencechronograms_cliente"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("funcionario_id") REFERENCES "confidencechronograms_funcionario"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "confidencechronograms_cronograma" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"estrutura"	varchar(200) NOT NULL,
	"proprietario"	varchar(80) NOT NULL,
	"endereco"	varchar(200) NOT NULL,
	"tempo_total"	varchar(30) NOT NULL,
	"valor_total"	decimal NOT NULL,
	"date_added"	datetime NOT NULL,
	"date_update"	datetime NOT NULL,
	"cliente_id"	integer NOT NULL,
	"funcionario_id"	integer,
	FOREIGN KEY("cliente_id") REFERENCES "confidencechronograms_cliente"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("funcionario_id") REFERENCES "confidencechronograms_funcionario"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "confidencechronograms_funcionario" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"nome"	varchar(60) NOT NULL,
	"cpf"	varchar(11),
	"rg"	varchar(9),
	"dt_nascimento"	datetime,
	"sexo"	varchar(1) NOT NULL,
	"nacionalidade"	varchar(30),
	"naturalidade"	varchar(30),
	"profissao"	varchar(100),
	"estado_civil"	varchar(15),
	"rua"	varchar(60) NOT NULL,
	"numero"	varchar(10) NOT NULL,
	"complemento"	varchar(30),
	"bairro"	varchar(30),
	"cidade"	varchar(30),
	"cep"	varchar(8),
	"uf"	varchar(2),
	"email"	varchar(60) NOT NULL,
	"fone"	varchar(16) NOT NULL,
	"dt_admissao"	datetime,
	"cargo"	varchar(20),
	"salario"	real,
	"date_added"	datetime NOT NULL,
	"date_update"	datetime NOT NULL,
	"usuario_id"	integer NOT NULL,
	FOREIGN KEY("usuario_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "confidencechronograms_tarefa_taxas" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"tarefa_id"	integer NOT NULL,
	"taxa_id"	integer NOT NULL,
	FOREIGN KEY("taxa_id") REFERENCES "confidencechronograms_taxa"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("tarefa_id") REFERENCES "confidencechronograms_tarefa"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "confidencechronograms_tarefa_materiais" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"tarefa_id"	integer NOT NULL,
	"material_id"	integer NOT NULL,
	FOREIGN KEY("material_id") REFERENCES "confidencechronograms_material"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("tarefa_id") REFERENCES "confidencechronograms_tarefa"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "confidencechronograms_tarefa_maos_de_obra" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"tarefa_id"	integer NOT NULL,
	"mao_de_obra_id"	integer NOT NULL,
	FOREIGN KEY("tarefa_id") REFERENCES "confidencechronograms_tarefa"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("mao_de_obra_id") REFERENCES "confidencechronograms_mao_de_obra"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "confidencechronograms_tarefa" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"ident"	varchar(4) NOT NULL,
	"nome"	varchar(40) NOT NULL,
	"descricao"	text NOT NULL,
	"dt_inicial"	date NOT NULL,
	"dt_final"	date NOT NULL,
	"progresso"	varchar(3) NOT NULL,
	"dependencias"	varchar(10) NOT NULL,
	"date_added"	datetime NOT NULL,
	"date_update"	datetime NOT NULL,
	"cronograma_id"	integer NOT NULL,
	FOREIGN KEY("cronograma_id") REFERENCES "confidencechronograms_cronograma"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "confidencechronograms_taxa" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"nome"	varchar(60) NOT NULL,
	"unidade"	varchar(20) NOT NULL,
	"valor_unitario"	decimal NOT NULL,
	"quantidade"	decimal NOT NULL,
	"cronograma_id"	integer NOT NULL,
	"orgao_id"	integer NOT NULL,
	FOREIGN KEY("orgao_id") REFERENCES "confidencechronograms_orgao"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("cronograma_id") REFERENCES "confidencechronograms_cronograma"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "confidencechronograms_orgao" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"nome"	varchar(200) NOT NULL,
	"cnpj"	varchar(18),
	"email"	varchar(60),
	"fone"	varchar(16) NOT NULL,
	"date_added"	datetime NOT NULL,
	"date_update"	datetime NOT NULL
);
CREATE TABLE IF NOT EXISTS "confidencechronograms_mao_de_obra_funcionarios_da_obra" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"mao_de_obra_id"	integer NOT NULL,
	"funcionario_da_obra_id"	integer NOT NULL,
	FOREIGN KEY("funcionario_da_obra_id") REFERENCES "confidencechronograms_funcionario_da_obra"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("mao_de_obra_id") REFERENCES "confidencechronograms_mao_de_obra"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "confidencechronograms_mao_de_obra" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"nome"	varchar(200) NOT NULL,
	"unidade"	varchar(20) NOT NULL,
	"valor_unitario"	decimal NOT NULL,
	"quantidade"	decimal NOT NULL,
	"date_added"	datetime NOT NULL,
	"date_update"	datetime NOT NULL,
	"cronograma_id"	integer NOT NULL,
	"empreiteira_id"	integer,
	FOREIGN KEY("empreiteira_id") REFERENCES "confidencechronograms_empreiteira"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("cronograma_id") REFERENCES "confidencechronograms_cronograma"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "confidencechronograms_funcionario_da_obra" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"nome"	varchar(60) NOT NULL,
	"cpf"	varchar(11),
	"rg"	varchar(9),
	"dt_nascimento"	datetime,
	"sexo"	varchar(1) NOT NULL,
	"nacionalidade"	varchar(30),
	"naturalidade"	varchar(30),
	"profissao"	varchar(100),
	"estado_civil"	varchar(15),
	"rua"	varchar(60) NOT NULL,
	"numero"	varchar(10) NOT NULL,
	"complemento"	varchar(30),
	"bairro"	varchar(30),
	"cidade"	varchar(30),
	"cep"	varchar(8),
	"uf"	varchar(2),
	"email"	varchar(60) NOT NULL,
	"fone"	varchar(16) NOT NULL,
	"date_added"	datetime NOT NULL,
	"date_update"	datetime NOT NULL,
	"empreiteira_id"	integer NOT NULL,
	FOREIGN KEY("empreiteira_id") REFERENCES "confidencechronograms_empreiteira"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "confidencechronograms_empreiteira_cronogramas" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"empreiteira_id"	integer NOT NULL,
	"cronograma_id"	integer NOT NULL,
	FOREIGN KEY("cronograma_id") REFERENCES "confidencechronograms_cronograma"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("empreiteira_id") REFERENCES "confidencechronograms_empreiteira"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "confidencechronograms_empreiteira" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"nome"	varchar(200) NOT NULL,
	"cnpj"	varchar(18),
	"email"	varchar(60),
	"fone"	varchar(16) NOT NULL,
	"date_added"	datetime NOT NULL,
	"date_update"	datetime NOT NULL
);
CREATE TABLE IF NOT EXISTS "confidencechronograms_deposito" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"nome"	varchar(200) NOT NULL,
	"cnpj"	varchar(18),
	"email"	varchar(60),
	"fone"	varchar(16) NOT NULL,
	"date_added"	datetime NOT NULL,
	"date_update"	datetime NOT NULL
);
CREATE TABLE IF NOT EXISTS "confidencechronograms_cliente" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"nome"	varchar(60) NOT NULL,
	"cpf"	varchar(11),
	"rg"	varchar(9),
	"dt_nascimento"	datetime,
	"sexo"	varchar(1) NOT NULL,
	"nacionalidade"	varchar(30),
	"naturalidade"	varchar(30),
	"profissao"	varchar(100),
	"estado_civil"	varchar(15),
	"rua"	varchar(60) NOT NULL,
	"numero"	varchar(10) NOT NULL,
	"complemento"	varchar(30),
	"bairro"	varchar(30),
	"cidade"	varchar(30),
	"cep"	varchar(8),
	"uf"	varchar(2),
	"email"	varchar(60) NOT NULL,
	"fone"	varchar(16) NOT NULL,
	"date_added"	datetime NOT NULL,
	"date_update"	datetime NOT NULL,
	"usuario_id"	integer NOT NULL,
	FOREIGN KEY("usuario_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "confidencechronograms_categoria" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"nome"	varchar(200) NOT NULL,
	"date_added"	datetime NOT NULL,
	"date_update"	datetime NOT NULL
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"name"	varchar(150) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "auth_user" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"username"	varchar(150) NOT NULL UNIQUE,
	"first_name"	varchar(30) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"last_name"	varchar(150) NOT NULL
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"action_time"	datetime NOT NULL,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	integer NOT NULL,
	"action_flag"	smallint unsigned NOT NULL CHECK("action_flag">=0),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"user_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user_groups" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"user_id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_material_deposito_id_79aa36a8" ON "confidencechronograms_material" (
	"deposito_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_material_cronograma_id_6820879a" ON "confidencechronograms_material" (
	"cronograma_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_material_categoria_id_34c1c46e" ON "confidencechronograms_material" (
	"categoria_id"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_comentario_funcionario_id_53909ed3" ON "confidencechronograms_comentario" (
	"funcionario_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_comentario_cliente_id_5908e3b9" ON "confidencechronograms_comentario" (
	"cliente_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_cronograma_funcionario_id_8976b827" ON "confidencechronograms_cronograma" (
	"funcionario_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_cronograma_cliente_id_eb22e223" ON "confidencechronograms_cronograma" (
	"cliente_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_funcionario_usuario_id_9424584d" ON "confidencechronograms_funcionario" (
	"usuario_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_tarefa_taxas_taxa_id_b8be58a9" ON "confidencechronograms_tarefa_taxas" (
	"taxa_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_tarefa_taxas_tarefa_id_ce4e3963" ON "confidencechronograms_tarefa_taxas" (
	"tarefa_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "confidencechronograms_tarefa_taxas_tarefa_id_taxa_id_f518b7dc_uniq" ON "confidencechronograms_tarefa_taxas" (
	"tarefa_id",
	"taxa_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_tarefa_materiais_material_id_79972661" ON "confidencechronograms_tarefa_materiais" (
	"material_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_tarefa_materiais_tarefa_id_3bdff7b9" ON "confidencechronograms_tarefa_materiais" (
	"tarefa_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "confidencechronograms_tarefa_materiais_tarefa_id_material_id_cda4df46_uniq" ON "confidencechronograms_tarefa_materiais" (
	"tarefa_id",
	"material_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_tarefa_maos_de_obra_mao_de_obra_id_92c39a22" ON "confidencechronograms_tarefa_maos_de_obra" (
	"mao_de_obra_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_tarefa_maos_de_obra_tarefa_id_2957ea2e" ON "confidencechronograms_tarefa_maos_de_obra" (
	"tarefa_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "confidencechronograms_tarefa_maos_de_obra_tarefa_id_mao_de_obra_id_f8748bff_uniq" ON "confidencechronograms_tarefa_maos_de_obra" (
	"tarefa_id",
	"mao_de_obra_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_tarefa_cronograma_id_4ac395e8" ON "confidencechronograms_tarefa" (
	"cronograma_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_taxa_orgao_id_cac8021e" ON "confidencechronograms_taxa" (
	"orgao_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_taxa_cronograma_id_49cc9c83" ON "confidencechronograms_taxa" (
	"cronograma_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_mao_de_obra_funcionarios_da_obra_funcionario_da_obra_id_a965bfc2" ON "confidencechronograms_mao_de_obra_funcionarios_da_obra" (
	"funcionario_da_obra_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_mao_de_obra_funcionarios_da_obra_mao_de_obra_id_fc0b3ee8" ON "confidencechronograms_mao_de_obra_funcionarios_da_obra" (
	"mao_de_obra_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "confidencechronograms_mao_de_obra_funcionarios_da_obra_mao_de_obra_id_funcionario_da_obra_id_cdeaec1c_uniq" ON "confidencechronograms_mao_de_obra_funcionarios_da_obra" (
	"mao_de_obra_id",
	"funcionario_da_obra_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_mao_de_obra_empreiteira_id_28ce9091" ON "confidencechronograms_mao_de_obra" (
	"empreiteira_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_mao_de_obra_cronograma_id_0f550241" ON "confidencechronograms_mao_de_obra" (
	"cronograma_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_funcionario_da_obra_empreiteira_id_12716103" ON "confidencechronograms_funcionario_da_obra" (
	"empreiteira_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_empreiteira_cronogramas_cronograma_id_7a12878a" ON "confidencechronograms_empreiteira_cronogramas" (
	"cronograma_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_empreiteira_cronogramas_empreiteira_id_8ac8dea6" ON "confidencechronograms_empreiteira_cronogramas" (
	"empreiteira_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "confidencechronograms_empreiteira_cronogramas_empreiteira_id_cronograma_id_666ae7e5_uniq" ON "confidencechronograms_empreiteira_cronogramas" (
	"empreiteira_id",
	"cronograma_id"
);
CREATE INDEX IF NOT EXISTS "confidencechronograms_cliente_usuario_id_d57bcf61" ON "confidencechronograms_cliente" (
	"usuario_id"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" (
	"user_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_group_id_97559544" ON "auth_user_groups" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" (
	"user_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
COMMIT;
