from datetime import datetime, timedelta
from urllib.parse import urlparse

from django.conf import settings
from storages.backends.azure_storage import AzureStorage

from azure.storage.blob import (
    BlobServiceClient,
    generate_blob_sas,
    BlobSasPermissions,
)


class AzureMediaStorage(AzureStorage):
    account_name = settings.AZURE_ACCOUNT_NAME
    account_key = settings.AZURE_ACCOUNT_KEY
    azure_container = settings.AZURE_CONTAINER
    expiration_secs = None
    overwrite_files = False

    def url(self, name):
        return name


class AzureFileProxy:
    @staticmethod
    def _candidate_containers():
        primary = (getattr(settings, "AZURE_CONTAINER", "") or "").strip()
        fallbacks = []

        extra = (getattr(settings, "AZURE_CONTAINER_FALLBACKS", "") or "").strip()
        if extra:
            fallbacks.extend([c.strip() for c in extra.split(",") if c.strip()])

        # defaults comunes
        for c in ("media", "cursos"):
            if c and c not in fallbacks:
                fallbacks.append(c)

        containers = []
        if primary:
            containers.append(primary)
        for c in fallbacks:
            if c and c not in containers:
                containers.append(c)

        return containers

    @staticmethod
    def _normalize_blob_name(blob_name: str) -> str:
        """
        Normaliza:
        - URL completa -> path del blob sin contenedor
        - backslashes -> slashes
        - quita slash inicial
        """
        if not blob_name:
            return ""

        s = str(blob_name).strip().replace("\\", "/")

        # Si viene como URL
        if s.startswith("http://") or s.startswith("https://"):
            parsed = urlparse(s)
            path = parsed.path.lstrip("/")  # "container/folder/file"
            parts = path.split("/", 1)
            s = parts[1] if len(parts) == 2 else path

        return s.lstrip("/")

    @staticmethod
    def _blob_name_variants(blob_name: str):
        """
        Genera variantes para encontrar el blob aunque venga con prefijo del contenedor:
          - "cursos/experiencia/a.pdf" -> "experiencia/a.pdf"
          - "media/..." -> "..."
        """
        base = AzureFileProxy._normalize_blob_name(blob_name)
        if not base:
            return []

        variants = [base]

        # si viene prefijado con un contenedor, lo quitamos
        for container in AzureFileProxy._candidate_containers():
            prefix = f"{container.strip()}/"
            if base.startswith(prefix):
                variants.append(base[len(prefix):])

        # elimina duplicados manteniendo orden
        seen = set()
        out = []
        for v in variants:
            if v and v not in seen:
                seen.add(v)
                out.append(v)
        return out

    @staticmethod
    def _get_blob_client(container: str, blob_name: str):
        bsc = BlobServiceClient.from_connection_string(settings.AZURE_CONNECTION_STRING)
        return bsc.get_blob_client(container=container, blob=blob_name)

    @staticmethod
    def download_blob(blob_name: str):
        variants = AzureFileProxy._blob_name_variants(blob_name)
        if not variants:
            raise FileNotFoundError("Nombre de archivo vacío")

        last_error = None
        for container in AzureFileProxy._candidate_containers():
            for name_try in variants:
                try:
                    blob_client = AzureFileProxy._get_blob_client(container, name_try)
                    props = blob_client.get_blob_properties()
                    content = blob_client.download_blob().readall()
                    return content, props
                except Exception as e:
                    last_error = e

        raise FileNotFoundError(f"Archivo no encontrado en Azure: {variants}. Detalle: {last_error}")

    @staticmethod
    def generate_sas_url(blob_name: str, expiry_hours: int = 1) -> str:
        variants = AzureFileProxy._blob_name_variants(blob_name)
        if not variants:
            raise FileNotFoundError("Nombre de archivo vacío")

        last_error = None
        for container in AzureFileProxy._candidate_containers():
            for name_try in variants:
                try:
                    blob_client = AzureFileProxy._get_blob_client(container, name_try)
                    blob_client.get_blob_properties()  # valida existencia

                    sas_token = generate_blob_sas(
                        account_name=settings.AZURE_ACCOUNT_NAME,
                        container_name=container,
                        blob_name=name_try,
                        account_key=settings.AZURE_ACCOUNT_KEY,
                        permission=BlobSasPermissions(read=True),
                        expiry=datetime.utcnow() + timedelta(hours=expiry_hours),
                    )
                    return f"{blob_client.url}?{sas_token}"
                except Exception as e:
                    last_error = e

        raise FileNotFoundError(f"Archivo no encontrado en Azure: {variants}. Detalle: {last_error}")
