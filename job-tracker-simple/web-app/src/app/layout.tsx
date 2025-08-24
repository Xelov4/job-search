import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import '@mantine/core/styles.css'
import '@mantine/notifications/styles.css'

import { MantineProvider, ColorSchemeScript } from '@mantine/core'
import { Notifications } from '@mantine/notifications'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Job Tracker Simple - Suivi Personnel des Candidatures',
  description: 'Application simple pour suivre et gérer ses candidatures d\'emploi avec données LinkedIn Enhanced',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr">
      <head>
        <ColorSchemeScript />
      </head>
      <body className={inter.className}>
        <MantineProvider 
          theme={{
            primaryColor: 'blue',
            fontFamily: inter.style.fontFamily,
            headings: { fontFamily: inter.style.fontFamily },
            breakpoints: {
              xs: '30em',
              sm: '48em', 
              md: '64em',
              lg: '74em',
              xl: '90em',
            },
          }}
          defaultColorScheme="light"
        >
          <Notifications position="top-right" />
          {children}
        </MantineProvider>
      </body>
    </html>
  );
}
