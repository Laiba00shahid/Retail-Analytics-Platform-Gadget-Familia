"use client"

import Breadcrumb from "@/components/Common/Breadcrumb"
import { useSearchParams } from "next/navigation"

export default function ErrorPage() {
  const params = useSearchParams()
  const msg = params.get("msg")

  return (
    <>
      <Breadcrumb title="Error" pages={["Error"]} />

      <div className="flex flex-col justify-center items-center h-[70vh] text-center px-6">

        <h1 className="text-4xl font-bold mb-4" style={{ color: "#1976d2" }}>
          Something Went Wrong
        </h1>

        <p className="text-lg text-black max-w-xl leading-relaxed">
          {msg || "Unknown error occurred"}
        </p>

      </div>
    </>
  )
}
