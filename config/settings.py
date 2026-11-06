import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
BASE_DIR=Path(__file__).resolve().parent.parent; load_dotenv(BASE_DIR/".env")
SECRET_KEY=os.getenv("SECRET_KEY","unsafe-development-key-change-me"); DEBUG=os.getenv("DEBUG","False").lower()=="true"
ALLOWED_HOSTS=[x.strip() for x in os.getenv("ALLOWED_HOSTS","127.0.0.1,localhost").split(",")]
INSTALLED_APPS=["django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles","rest_framework","django_filters","drf_spectacular","shop"]
MIDDLEWARE=["django.middleware.security.SecurityMiddleware","django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware","django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF="config.urls"; WSGI_APPLICATION="config.wsgi.application"
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.debug","django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
DATABASES={"default":dj_database_url.parse(os.environ["DATABASE_URL"],conn_max_age=600)} if os.getenv("DATABASE_URL") else {"default":{"ENGINE":"django.db.backends.sqlite3","NAME":BASE_DIR/"db.sqlite3"}}
AUTH_PASSWORD_VALIDATORS=[{"NAME":"django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},{"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator"}]
LANGUAGE_CODE="en-us"; TIME_ZONE="UTC"; USE_I18N=True; USE_TZ=True; STATIC_URL="static/"; DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
REST_FRAMEWORK={"DEFAULT_AUTHENTICATION_CLASSES":["rest_framework.authentication.BasicAuthentication","rest_framework.authentication.SessionAuthentication"],"DEFAULT_PERMISSION_CLASSES":["rest_framework.permissions.IsAuthenticatedOrReadOnly"],"DEFAULT_FILTER_BACKENDS":["django_filters.rest_framework.DjangoFilterBackend","rest_framework.filters.SearchFilter","rest_framework.filters.OrderingFilter"],"DEFAULT_PAGINATION_CLASS":"rest_framework.pagination.PageNumberPagination","PAGE_SIZE":10,"DEFAULT_SCHEMA_CLASS":"drf_spectacular.openapi.AutoSchema","DEFAULT_RENDERER_CLASSES":["rest_framework.renderers.JSONRenderer"]}
SPECTACULAR_SETTINGS={"TITLE":"E-commerce Inventory API","DESCRIPTION":"Product and order workflows","VERSION":"1.0.0"}
