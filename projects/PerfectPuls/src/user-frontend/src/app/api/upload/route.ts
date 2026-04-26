import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    
    // Forward the request to your FastAPI backend
    const backendResponse = await fetch("http://localhost:8000/api/process-pdf", {
      method: "POST",
      body: formData,
    });

    if (backendResponse.ok) {
      const data = await backendResponse.json();
      return NextResponse.json(data);
    } else {
      const error = await backendResponse.text();
      return NextResponse.json(
        { error: `Backend error: ${error}` },
        { status: backendResponse.status }
      );
    }
  } catch (error) {
    console.error("Upload API error:", error);
    return NextResponse.json(
      { error: "Failed to upload file" },
      { status: 500 }
    );
  }
}