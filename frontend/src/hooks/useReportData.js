import { useState, useEffect } from "react";
import apiClient from "../lib/apiClient";

export function useReportData(sessionId) {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!sessionId) {
      setLoading(false);
      setError("No session ID provided.");
      return;
    }

    const fetchReport = async () => {
      try {
        const response = await apiClient.get(
          `/api/v1/interview/report/${sessionId}`,
        );
        setReport(response.data);
      } catch (err) {
        setError(err.response?.data?.detail || "Could not load report.");
      } finally {
        setLoading(false);
      }
    };

    fetchReport();
  }, [sessionId]);

  return { report, loading, error };
}
