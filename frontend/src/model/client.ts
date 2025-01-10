export interface Client {
    email: string;
    payment_address: Address;
    delivery_address: Address;
    nip;
    password;
    company_name;
}

export interface Address {
    voivodeship: string;
    city: string;
    street: string;
    postal_code: string;
    house_number: string;
}