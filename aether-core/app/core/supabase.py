import os
from supabase import create_client, Client

url: str = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
key: str = os.getenv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY")
service_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Use service role key for backend operations if available
supabase: Client = create_client(url, service_key if service_key else key)
