'use client'

import { createClient } from '@/utils/supabase/client'

export async function logout() {
  const supabase = createClient()
  await supabase.auth.signOut()
  window.location.href = '/signin'
}
