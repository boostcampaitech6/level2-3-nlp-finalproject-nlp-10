import React from 'react'
import { LineChart } from '@mui/x-charts/LineChart';
import dayjs from "dayjs";

const companyClosePrice = [68600, 69700, 69600, 69600, 69600, 70900, 70900, 69900, 70300, 70500, 70500, 70500, 70400, 70800, 72200, 72800, 72500, 72500, 72500, 72700]
const stockDateList = ["2023-11-01",
  "2023-11-02",
  "2023-11-03",
  "2023-11-04",
  "2023-11-05",
  "2023-11-06",
  "2023-11-07",
  "2023-11-08",
  "2023-11-09",
  "2023-11-10",
  "2023-11-11",
  "2023-11-12",
  "2023-11-13",
  "2023-11-14",
  "2023-11-15",
  "2023-11-16",
  "2023-11-17",
  "2023-11-18",
  "2023-11-19",
  "2023-11-20"]
const stockDate = stockDateList.map((date) => new Date(date.split('-')))
export default function StockInfo() {
  console.log(stockDate)
  return (
    <>
      <LineChart skipAnimation
        xAxis={[
          {
            data: stockDate,
            scaleType: 'time',
            valueFormatter: (date) => dayjs(date).format("YY MMM DD"),
            tickLabelStyle: {
              fontSize: 10
            }
          }
        ]}
        yAxis={[
          {
            tickLabelStyle: {
              fontSize: 10
            }
          }
        ]}
        series={[
          {
            curve: "linear",
            showMark: false,
            label: "Stock Close Price",
            data: companyClosePrice,
          },
        ]}
        width={450}
        height={230}
        slotProps={{ legend: { hidden: true } }}
      />
    </>
  )
}
