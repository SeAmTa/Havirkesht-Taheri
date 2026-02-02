CREATE TABLE IF NOT EXISTS cars (
    id BIGINT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255),
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT pk_cars PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT pk_alembic_version PRIMARY KEY (version_num)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS bulk_sms_job (
    id BIGINT NOT NULL AUTO_INCREMENT,
    job_id VARCHAR(36),
    status VARCHAR(20),
    pattern_code VARCHAR(50),
    total_farmers INT,
    processed_farmers INT,
    succeeded_farmers INT,
    failed_farmers INT,
    completed_at TIMESTAMP NULL,
    farmer_ids JSON,
    succeeded_farmer_ids JSON,
    failed_farmer_ids JSON,
    failed_sms_details JSON,
    config JSON,
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT pk_bulk_sms_job PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE INDEX idx_bulk_sms_job_job_id ON bulk_sms_job (job_id);


CREATE TABLE IF NOT EXISTS driver (
    id BIGINT NOT NULL AUTO_INCREMENT,

    name VARCHAR(255),
    last_name VARCHAR(255),
    national_code VARCHAR(10),
    phone_number VARCHAR(11),

    car_id BIGINT,
    license_plate VARCHAR(50),
    capacity_ton DOUBLE,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_driver PRIMARY KEY (id),
    CONSTRAINT fk_driver_car
        FOREIGN KEY (car_id)
        REFERENCES cars(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS roles (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50),
    scopes JSON,
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_roles PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS province (
    id BIGINT NOT NULL AUTO_INCREMENT,
    province VARCHAR(255),
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_province PRIMARY KEY (id),
    CONSTRAINT ux_province_province UNIQUE (province)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS supervisor (
    id BIGINT NOT NULL AUTO_INCREMENT,

    name VARCHAR(255),
    national_id BIGINT,
    degree VARCHAR(255),
    phone BIGINT,
    shaba_id VARCHAR(255),
    bank_name VARCHAR(255),
    address VARCHAR(255),
    capacity INT,
    supervision_permit VARCHAR(255),
    lat DOUBLE,
    lng DOUBLE,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_supervisor PRIMARY KEY (id),
    CONSTRAINT ux_supervisor_national_id UNIQUE (national_id),
    CONSTRAINT ux_supervisor_shaba_id UNIQUE (shaba_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS token_blacklist (
    id BIGINT NOT NULL AUTO_INCREMENT,
    token VARCHAR(255),
    blacklisted_at TIMESTAMP NULL,
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_token_blacklist PRIMARY KEY (id),
    CONSTRAINT ux_token_blacklist_token UNIQUE (token)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS measure_unit (
    id BIGINT NOT NULL AUTO_INCREMENT,
    unit_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_measure_unit PRIMARY KEY (id),
    CONSTRAINT ux_measure_unit_unit_name UNIQUE (unit_name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS factory (
    id BIGINT NOT NULL AUTO_INCREMENT,
    factory_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_factory PRIMARY KEY (id),
    CONSTRAINT ux_factory_factory_name UNIQUE (factory_name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS payment_reason (
    id BIGINT NOT NULL AUTO_INCREMENT,
    reason_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_payment_reason PRIMARY KEY (id),
    CONSTRAINT ux_payment_reason_reason_name UNIQUE (reason_name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS crop_year (
    id BIGINT NOT NULL AUTO_INCREMENT,
    crop_year_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_crop_year PRIMARY KEY (id),
    CONSTRAINT ux_crop_year_crop_year_name UNIQUE (crop_year_name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS farmer (
    id BIGINT NOT NULL AUTO_INCREMENT,

    national_id VARCHAR(10) NOT NULL,
    full_name VARCHAR(255),
    father_name VARCHAR(255),
    phone_number VARCHAR(11),

    sheba_number_1 VARCHAR(26),
    sheba_number_2 VARCHAR(26),
    card_number VARCHAR(16),

    address VARCHAR(255),

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_farmer PRIMARY KEY (id),
    CONSTRAINT ux_farmer_national_id UNIQUE (national_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS city (
    id BIGINT NOT NULL AUTO_INCREMENT,
    city VARCHAR(255) NOT NULL,
    province_id BIGINT NOT NULL,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_city PRIMARY KEY (id),
    CONSTRAINT ux_city_city UNIQUE (city),
    CONSTRAINT fk_city_province
        FOREIGN KEY (province_id)
        REFERENCES province(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS village (
    id BIGINT NOT NULL AUTO_INCREMENT,
    village VARCHAR(255) NOT NULL,
    city_id BIGINT NOT NULL,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_village PRIMARY KEY (id),
    CONSTRAINT ux_village_village UNIQUE (village),
    CONSTRAINT fk_village_city
        FOREIGN KEY (city_id)
        REFERENCES city(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS pesticide (
    id BIGINT NOT NULL AUTO_INCREMENT,
    pesticide_name VARCHAR(255) NOT NULL,
    measure_unit_id BIGINT NOT NULL,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_pesticide PRIMARY KEY (id),
    CONSTRAINT ux_pesticide_pesticide_name UNIQUE (pesticide_name),
    CONSTRAINT fk_pesticide_measure_unit
        FOREIGN KEY (measure_unit_id)
        REFERENCES measure_unit(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS seed (
    id BIGINT NOT NULL AUTO_INCREMENT,
    seed_name VARCHAR(255) NOT NULL,
    measure_unit_id BIGINT NOT NULL,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_seed PRIMARY KEY (id),
    CONSTRAINT ux_seed_seed_name UNIQUE (seed_name),
    CONSTRAINT fk_seed_measure_unit
        FOREIGN KEY (measure_unit_id)
        REFERENCES measure_unit(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS factory_commitment_tonnage (
    id BIGINT NOT NULL AUTO_INCREMENT,

    factory_id BIGINT NOT NULL,
    crop_year_id BIGINT NOT NULL,
    commited_tonnage_amount DOUBLE,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_factory_commitment_tonnage PRIMARY KEY (id),

    CONSTRAINT fk_fct_factory
        FOREIGN KEY (factory_id)
        REFERENCES factory(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_fct_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS users (
    id BIGINT NOT NULL AUTO_INCREMENT,

    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    fullname VARCHAR(255),
    phone_number VARCHAR(20),
    email VARCHAR(255),
    disabled BOOLEAN NOT NULL DEFAULT 0,

    role_id INT NOT NULL,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_users PRIMARY KEY (id),
    CONSTRAINT ux_users_username UNIQUE (username),

    CONSTRAINT fk_users_role
        FOREIGN KEY (role_id)
        REFERENCES roles(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS factory_payment (
    id BIGINT NOT NULL AUTO_INCREMENT,

    user_id BIGINT NOT NULL,
    crop_year_id BIGINT NOT NULL,
    factory_id BIGINT NOT NULL,

    title VARCHAR(255),
    `date` DATETIME NULL,
    price DOUBLE,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_factory_payment PRIMARY KEY (id),

    CONSTRAINT fk_factory_payment_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_factory_payment_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_factory_payment_factory
        FOREIGN KEY (factory_id)
        REFERENCES factory(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS factory_pesticide (
    id BIGINT NOT NULL AUTO_INCREMENT,

    factory_id BIGINT NOT NULL,
    pesticide_id BIGINT NOT NULL,
    crop_year_id BIGINT NOT NULL,

    amount DOUBLE,
    farmer_price DOUBLE,
    factory_price DOUBLE,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_factory_pesticide PRIMARY KEY (id),

    CONSTRAINT fk_factory_pesticide_factory
        FOREIGN KEY (factory_id)
        REFERENCES factory(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_factory_pesticide_pesticide
        FOREIGN KEY (pesticide_id)
        REFERENCES pesticide(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_factory_pesticide_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS factory_seed (
    id BIGINT NOT NULL AUTO_INCREMENT,

    factory_id BIGINT NOT NULL,
    seed_id BIGINT NOT NULL,
    crop_year_id BIGINT NOT NULL,

    amount DOUBLE,
    farmer_price DOUBLE,
    factory_price DOUBLE,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_factory_seed PRIMARY KEY (id),

    CONSTRAINT fk_factory_seed_factory
        FOREIGN KEY (factory_id)
        REFERENCES factory(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_factory_seed_seed
        FOREIGN KEY (seed_id)
        REFERENCES seed(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_factory_seed_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS factory_sugar (
    id BIGINT NOT NULL AUTO_INCREMENT,

    factory_id BIGINT NOT NULL,
    crop_year_id BIGINT NOT NULL,

    sugar_weight_received_factory DOUBLE,
    sugar_price_received_factory DOUBLE,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_factory_sugar PRIMARY KEY (id),

    CONSTRAINT fk_factory_sugar_factory
        FOREIGN KEY (factory_id)
        REFERENCES factory(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_factory_sugar_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS factory_waste (
    id BIGINT NOT NULL AUTO_INCREMENT,

    factory_id BIGINT NOT NULL,
    crop_year_id BIGINT NOT NULL,

    waste_weight_received_factory DOUBLE,
    waste_price_received_factory DOUBLE,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_factory_waste PRIMARY KEY (id),

    CONSTRAINT fk_factory_waste_factory
        FOREIGN KEY (factory_id)
        REFERENCES factory(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_factory_waste_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS farmers_guarantee (
    id BIGINT NOT NULL AUTO_INCREMENT,

    guarantor_farmer_id BIGINT NOT NULL,
    guaranteed_farmer_id BIGINT NOT NULL,
    crop_year_id BIGINT NOT NULL,

    guarantee_price DOUBLE,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_farmers_guarantee PRIMARY KEY (id),

    CONSTRAINT fk_fg_guarantor_farmer
        FOREIGN KEY (guarantor_farmer_id)
        REFERENCES farmer(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_fg_guaranteed_farmer
        FOREIGN KEY (guaranteed_farmer_id)
        REFERENCES farmer(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_fg_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS farmers_invoice_payed (
    id BIGINT NOT NULL AUTO_INCREMENT,

    farmer_id BIGINT NOT NULL,
    crop_year_id BIGINT NOT NULL,
    payed BOOLEAN NOT NULL DEFAULT 0,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_farmers_invoice_payed PRIMARY KEY (id),

    CONSTRAINT fk_fip_farmer
        FOREIGN KEY (farmer_id)
        REFERENCES farmer(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_fip_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS farmers_load (
    id BIGINT NOT NULL AUTO_INCREMENT,

    farmer_id BIGINT NOT NULL,
    factory_id BIGINT NOT NULL,
    crop_year_id BIGINT NOT NULL,

    `date` VARCHAR(255),
    load_number VARCHAR(255),
    driver_name VARCHAR(255),
    phone_number VARCHAR(20),

    total_weight DOUBLE,
    dirt_weight DOUBLE,
    pest_weight DOUBLE,
    pure_weight DOUBLE,

    sugar_beet_polarity DOUBLE,
    price_per_kilo DOUBLE,

    rent_help DOUBLE,
    transportation_cost DOUBLE,

    quota_sugar_price DOUBLE,
    quota_pulp_price DOUBLE,
    pure_payable DOUBLE,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_farmers_load PRIMARY KEY (id),

    CONSTRAINT fk_farmers_load_farmer
        FOREIGN KEY (farmer_id)
        REFERENCES farmer(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_farmers_load_factory
        FOREIGN KEY (factory_id)
        REFERENCES factory(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_farmers_load_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS farmers_payment (
    id BIGINT NOT NULL AUTO_INCREMENT,

    payment_type BIGINT NOT NULL,
    farmer_id BIGINT NOT NULL,
    crop_year_id BIGINT NOT NULL,

    price DOUBLE,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_farmers_payment PRIMARY KEY (id),

    CONSTRAINT fk_farmers_payment_reason
        FOREIGN KEY (payment_type)
        REFERENCES payment_reason(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_farmers_payment_farmer
        FOREIGN KEY (farmer_id)
        REFERENCES farmer(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_farmers_payment_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS farmers_sugar_delivery (
    id BIGINT NOT NULL AUTO_INCREMENT,

    farmer_id BIGINT NOT NULL,
    crop_year_id BIGINT NOT NULL,

    sugar_delivered DOUBLE,
    sugar_deposit_amount DOUBLE,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_farmers_sugar_delivery PRIMARY KEY (id),

    CONSTRAINT fk_fsd_farmer
        FOREIGN KEY (farmer_id)
        REFERENCES farmer(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_fsd_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS farmers_waste_delivery (
    id BIGINT NOT NULL AUTO_INCREMENT,

    farmer_id BIGINT NOT NULL,
    crop_year_id BIGINT NOT NULL,

    waste_delivered DOUBLE,
    waste_deposit_amount DOUBLE,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_farmers_waste_delivery PRIMARY KEY (id),

    CONSTRAINT fk_fwd_farmer
        FOREIGN KEY (farmer_id)
        REFERENCES farmer(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_fwd_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS product (
    id BIGINT NOT NULL AUTO_INCREMENT,

    product_name VARCHAR(255) NOT NULL,
    measure_unit_id BIGINT NOT NULL,
    crop_year_id BIGINT NOT NULL,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_product PRIMARY KEY (id),
    CONSTRAINT ux_product_product_name UNIQUE (product_name),

    CONSTRAINT fk_product_measure_unit
        FOREIGN KEY (measure_unit_id)
        REFERENCES measure_unit(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_product_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS product_price (
    id BIGINT NOT NULL AUTO_INCREMENT,

    crop_year_id BIGINT NOT NULL,

    sugar_amount_per_ton_kg DOUBLE,
    sugar_price_per_kg DOUBLE,

    pulp_amount_per_ton_kg DOUBLE,
    pulp_price_per_kg DOUBLE,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_product_price PRIMARY KEY (id),

    CONSTRAINT fk_product_price_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS purity_price (
    id BIGINT NOT NULL AUTO_INCREMENT,

    crop_year_id BIGINT NOT NULL,

    base_purity DOUBLE,
    base_purity_price DOUBLE,
    price_difference DOUBLE,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_purity_price PRIMARY KEY (id),

    CONSTRAINT fk_purity_price_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS commitment (
    id BIGINT NOT NULL AUTO_INCREMENT,

    crop_year_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    farmer_id BIGINT NOT NULL,
    village_id BIGINT NOT NULL,

    amount_of_land DOUBLE,
    withdrawal_amount DOUBLE,
    date_set DATETIME NULL,

    commitment_number VARCHAR(50) NOT NULL,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_commitment PRIMARY KEY (id),
    CONSTRAINT ux_commitment_number UNIQUE (commitment_number),

    CONSTRAINT fk_commitment_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_commitment_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_commitment_farmer
        FOREIGN KEY (farmer_id)
        REFERENCES farmer(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_commitment_village
        FOREIGN KEY (village_id)
        REFERENCES village(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS carriage (
    id BIGINT NOT NULL AUTO_INCREMENT,

    farmer_id BIGINT NOT NULL,
    village_id BIGINT NOT NULL,

    loading_date VARCHAR(10),
    weight DOUBLE,

    origin_id BIGINT,
    destination_id BIGINT,

    carriage_fee_per_ton DOUBLE,

    crop_year_id BIGINT NOT NULL,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_carriage PRIMARY KEY (id),

    CONSTRAINT fk_carriage_farmer
        FOREIGN KEY (farmer_id)
        REFERENCES farmer(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_carriage_village
        FOREIGN KEY (village_id)
        REFERENCES village(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_carriage_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS carriage_status (
    id BIGINT NOT NULL AUTO_INCREMENT,

    carriage_id BIGINT NOT NULL,
    driver_id BIGINT NOT NULL,
    carried BOOLEAN NOT NULL DEFAULT 0,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_carriage_status PRIMARY KEY (id),

    CONSTRAINT fk_carriage_status_carriage
        FOREIGN KEY (carriage_id)
        REFERENCES carriage(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_carriage_status_driver
        FOREIGN KEY (driver_id)
        REFERENCES driver(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS farmers_seed (
    id BIGINT NOT NULL AUTO_INCREMENT,

    commitment_id BIGINT NOT NULL,
    seed_id BIGINT NOT NULL,
    crop_year_id BIGINT NOT NULL,
    factory_id BIGINT NOT NULL,

    seed_amount DOUBLE,
    price DOUBLE,
    price_for_all_farmers_check_box BOOLEAN NOT NULL DEFAULT 0,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_farmers_seed PRIMARY KEY (id),

    CONSTRAINT fk_farmers_seed_commitment
        FOREIGN KEY (commitment_id)
        REFERENCES commitment(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_farmers_seed_seed
        FOREIGN KEY (seed_id)
        REFERENCES seed(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_farmers_seed_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_farmers_seed_factory
        FOREIGN KEY (factory_id)
        REFERENCES factory(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS farmers_pesticide (
    id BIGINT NOT NULL AUTO_INCREMENT,

    commitment_id BIGINT NOT NULL,
    pesticide_id BIGINT NOT NULL,
    crop_year_id BIGINT NOT NULL,
    factory_id BIGINT NOT NULL,

    pesticide_amount DOUBLE,
    price DOUBLE,
    price_for_all_farmers_check_box BOOLEAN NOT NULL DEFAULT 0,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT pk_farmers_pesticide PRIMARY KEY (id),

    CONSTRAINT fk_farmers_pesticide_commitment
        FOREIGN KEY (commitment_id)
        REFERENCES commitment(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_farmers_pesticide_pesticide
        FOREIGN KEY (pesticide_id)
        REFERENCES pesticide(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_farmers_pesticide_crop_year
        FOREIGN KEY (crop_year_id)
        REFERENCES crop_year(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_farmers_pesticide_factory
        FOREIGN KEY (factory_id)
        REFERENCES factory(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;
