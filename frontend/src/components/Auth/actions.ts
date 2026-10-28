'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'
import { createClient } from '../../utils/supabase/server'

export async function login(formData: FormData) {
  const supabase = await createClient()

  const email = formData.get('email')
  const password = formData.get('password')

  if (!email || !password) {
    redirect('/error?msg=Missing credentials')
  }

  const { error } = await supabase.auth.signInWithPassword({
    email: email.toString(),
    password: password.toString(),
  })

  if (error) {
    redirect(`/error?msg=${encodeURIComponent(error.message)}`)
  }

  revalidatePath('/', 'layout')
  redirect('/')
}

export async function signup(formData: FormData) {
  const supabase = await createClient()

  const email = formData.get('email')
  const password = formData.get('password')
  const confirm = formData.get('confirmPassword')

  if (!email || !password || !confirm) {
    redirect('/error?msg=Missing fields')
  }

  if (password.toString() !== confirm.toString()) {
    redirect('/error?msg=Password mismatch')
  }

  const { error } = await supabase.auth.signUp({
    email: email.toString(),
    password: password.toString(),
  })

  if (error) {
    redirect(`/error?msg=${encodeURIComponent(error.message)}`)
  }

  revalidatePath('/', 'layout')
  redirect('/signin')
}
