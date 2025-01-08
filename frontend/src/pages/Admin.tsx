import React, { useState } from "react";
import {
  Box,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import { DatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { Bar } from "react-chartjs-2";
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  ChartOptions,
  Legend,
  LinearScale,
  Tooltip,
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const Admin = () => {
  const [filters, setFilters] = useState({
    startDate: null,
    endDate: null,
  });
  const [data, setData] = useState([
    {
      numberOfTransports: 10,
      transportValue: 5000,
      destinationRegion: "Region A",
      destinationDistrict: "District 1",
    },
    {
      numberOfTransports: 15,
      transportValue: 7500,
      destinationRegion: "Region B",
      destinationDistrict: "District 2",
    },
    {
      numberOfTransports: 20,
      transportValue: 10000,
      destinationRegion: "Region C",
      destinationDistrict: "District 3",
    },
  ]);

  const fetchReports = async () => {
    try {
      // const response = await axios.get(`/api/orders/stats`, {
      //   params: {
      //     startDate: filters.startDate ? filters.startDate.toISOString() : undefined,
      //     endDate: filters.endDate ? filters.endDate.toISOString() : undefined,
      //   },
      // });
      // setData(response.data);
    } catch (error) {
      console.error("Error fetching reports:", error);
    }
  };

  const transportBarChartData = {
    labels: data.map((row) => row.destinationRegion),
    datasets: [
      {
        label: "Number of Transports",
        data: data.map((row) => row.numberOfTransports),
        backgroundColor: "rgba(75, 192, 192, 0.6)",
      },
    ],
  };

  const valueBarChartData = {
    labels: data.map((row) => row.destinationRegion),
    datasets: [
      {
        label: "Transport Value",
        data: data.map((row) => row.transportValue),
        backgroundColor: "rgba(153, 102, 255, 0.6)",
      },
    ],
  };

  const chartOptions: ChartOptions<"bar"> = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      tooltip: {
        mode: "index",
        intersect: false,
      },
    },
  };

  return (
    <Box sx={{ padding: "16px" }}>
      <Typography variant="h4" gutterBottom>
        Admin Panel - Reports
      </Typography>

      <Box
        sx={{
          display: "flex",
          gap: "16px",
          marginBottom: "24px",
          justifyContent: "space-evenly",
        }}
      >
        <LocalizationProvider dateAdapter={AdapterDateFns}>
          <DatePicker
            label="Start Date"
            value={filters.startDate}
            onChange={(newValue) =>
              setFilters({ ...filters, startDate: newValue })
            }
            renderInput={(params) => <TextField {...params} fullWidth />}
          />
          <DatePicker
            label="End Date"
            value={filters.endDate}
            onChange={(newValue) =>
              setFilters({ ...filters, endDate: newValue })
            }
            renderInput={(params) => <TextField {...params} fullWidth />}
          />
        </LocalizationProvider>

        <Button variant="contained" color="primary" onClick={fetchReports}>
          Generate Report
        </Button>
      </Box>

      <Box sx={{ display: "flex", gap: "24px", marginBottom: "24px" }}>
        <Box sx={{ flex: 1, height: "400px" }}>
          <Typography variant="h6" gutterBottom>
            Number of Transports (Bar Chart)
          </Typography>
          <Bar data={transportBarChartData} options={chartOptions} />
        </Box>

        <Box sx={{ flex: 1, height: "400px" }}>
          <Typography variant="h6" gutterBottom>
            Transport Value (Bar Chart)
          </Typography>
          <Bar data={valueBarChartData} options={chartOptions} />
        </Box>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Number of Transports</TableCell>
              <TableCell>Transport Value</TableCell>
              <TableCell>Destination Region</TableCell>
              <TableCell>Destination District</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((row, index) => (
              <TableRow key={index}>
                <TableCell>{row.numberOfTransports}</TableCell>
                <TableCell>{row.transportValue}</TableCell>
                <TableCell>{row.destinationRegion}</TableCell>
                <TableCell>{row.destinationDistrict}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default Admin;