from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    description: str = None
    database_url: str = 'sqlite+aiosqlite:///./cat_charity_fund.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    JWT_lifetime_seconds = 36000
    password_min = 3
    charity_project_name_max = 100
    attribute_length_slice = 10
    # Переменные для Google API
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = '-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDvmZ3NID/+BXeu\nr1h4rHPupbnXB6nSbgw81x/kGE8vUWVwF99sFdova7XtWHIIewp29fynuDpP+Q0v\nd0Nn/sbrbGY1sibEjkn2g3UwR/0t7d+ZUhfGWdhWol3YiZakMGE0Pu3MtjooRzr8\nFbxQZf6j9oVN01i1GGQs5FqYO7e3CWKxDef/A702M1M1VVcjBHfhCWjaFqepkHus\nKoGBsc+fVWbVlRS8wwqMFU/MNXlxRd90S8A+e87kzWGEyQDmCCgcnHcw4QK8IyR7\nEDNMSH53rdXNKQJJ/441ahOngLm8Xr3nBUT5JnF6d6wRsXio9Il85MUz+aln6R0m\nxDtQVEVLAgMBAAECggEAdb1qUxuu9pgfOQNHmX09Nx/PVACbDiIv91HLhR4BA4Kf\nM1c33nhakIUAkJKu7sXv3YeB0bVxSk1bkmCsChWkEJpjG63g6SP26qGs2730hzZm\nc4Ro1HrgGaqOLVNnaGWxzqfB2aAOsi5WqPvRXzzPxijlVtottEg5KepJLpfh7ppF\nqdIMo1MesfxrXUpU44ax3pvRnWFAPQL7IeTPCOV10i5I39kGBnpHD3VnrwmKAr33\nkbudexDHG4SUGTYaVAmfQhCxM1YkRGKRNqpygwEgU4jdt1BJVWaOlZNJjhlijVKL\nbRFRSWui7oqQk6aORa5fXF5ZNS3QprJhouP0x85fEQKBgQD7lACTPrPsrdZ94YJR\nFzxV75MmpKscIee/o++W62I9ojGxypPfgeFPTS3pjPyTM43qZw1+HVXo04Sz59mQ\nE4zn3HAK1m3EwREVGNlJmIxjIwMiDGQqtHh5Lk9TQFhyQPIBOJIH/dI29wvmPaFP\nR+OC5aXB/WOXwuXX4zl5Iw0kaQKBgQDzz7fBb5tSnEpA55OCUrDaw8f1G+eV4KW0\nav1sQTxiKX6WqyPBcJVUHdL4Gd4m//6CwR0JlRE+4VRh3CkhfUKCFFe8VCjjvRfJ\nX9ELSIlTT5HmKBtc2Er2oSKAOhxDU7v3rLQRbEMchSRZcOW43bX6CIfehB8OhDsD\nyP6OKPXVkwKBgQD0mmoUwBpgPIUXz3LNNTJMu6rvH5vetniFM/d3XVUfZ9u5aaVs\n4vMWD4xcT+AjnzSUe636uLsWrNGRuhMmqluN9B5b6zC+5JifUpGxpMiaeyhIqpOZ\nke6wo/4si5tzOwIRfdc+PeNt3bWMHtAALX1ff7kybBOxMqYWya7PwOy+QQKBgQC9\nzSflC4hkME1R57Waz9rkA2PHubh4ohD9ugidXM+wL1Nf4c0NCyME/8673A9oVwOA\nMOv1CLoLNIlnQWg3rPa4ozOF5hKK8CrzVoc7fHWDiL8w6GocxjjddKWSIyrbcvUy\no5zur1QzgKbChjQfzWGcS0XSgRJYT7JNiQw6CUMPxwKBgQDnNzly5U3OfZNg4Z/w\nYEScfTuSkCjEsk2hqCR60BivctQakt0TFAd14H9t2ffw6AYgBwxKkb0o/yapN76j\nwA80AE/38jK3ciUWL4lB1z04pUdz+cjUOqFD8+/L/7cFszG3CVBSMsAgK+HkwTpJ\n/IDtB+oQAPWhVSLPT0xVHXQXWw==\n-----END PRIVATE KEY-----\n'
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
