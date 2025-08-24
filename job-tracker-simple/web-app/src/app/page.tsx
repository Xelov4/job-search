'use client'

import { useState, useEffect } from 'react'
import {
  Container,
  Title,
  Text,
  Grid,
  Card,
  Badge,
  Button,
  Group,
  Select,
  TextInput,
  ActionIcon,
  Stack,
  Divider,
  Paper,
  SimpleGrid,
  Loader,
  Center,
  Rating,
  Modal,
  Textarea,
} from '@mantine/core'
import {
  IconSearch,
  IconExternalLink,
  IconBriefcase,
  IconStar,
  IconNotes,
  IconMapPin,
  IconHome,
  IconBuilding
} from '@tabler/icons-react'
import { notifications } from '@mantine/notifications'
import { useDisclosure } from '@mantine/hooks'

import { JobOffer, DashboardStats, jobOperations } from '@/lib/supabase'

// Composant pour les statistiques
function StatsCards({ stats }: { stats: DashboardStats }) {
  const statsData = [
    {
      title: 'Total Emplois',
      value: stats.total_jobs,
      color: 'blue',
      icon: IconBriefcase
    },
    {
      title: 'Intéressants',
      value: stats.interested_count,
      color: 'orange',
      icon: IconStar
    },
    {
      title: 'Candidatures',
      value: stats.applied_count,
      color: 'green',
      icon: IconExternalLink
    },
    {
      title: 'Télétravail',
      value: stats.remote_count,
      color: 'violet',
      icon: IconHome
    }
  ]

  return (
    <SimpleGrid cols={{ base: 2, md: 4 }} spacing="md" mb="xl">
      {statsData.map((stat) => (
        <Card key={stat.title} padding="md" radius="md" withBorder>
          <Group justify="space-between">
            <div>
              <Text c="dimmed" size="sm" fw={700} tt="uppercase">
                {stat.title}
              </Text>
              <Text fw={700} size="xl">
                {stat.value}
              </Text>
            </div>
            <ActionIcon
              color={stat.color}
              size={38}
              radius="md"
              variant="light"
            >
              <stat.icon size={24} stroke={1.5} />
            </ActionIcon>
          </Group>
        </Card>
      ))}
    </SimpleGrid>
  )
}

// Composant pour une carte d'emploi
function JobCard({ 
  job, 
  onStatusChange, 
  onPriorityChange, 
  onNotesUpdate 
}: {
  job: JobOffer
  onStatusChange: (jobId: string, status: string) => void
  onPriorityChange: (jobId: string, priority: number) => void
  onNotesUpdate: (jobId: string, notes: string) => void
}) {
  const [opened, { open, close }] = useDisclosure(false)
  const [notes, setNotes] = useState(job.notes || '')

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      discovered: 'blue',
      interested: 'orange',
      applied: 'green',
      interview: 'violet',
      rejected: 'red',
      archived: 'gray'
    }
    return colors[status] || 'gray'
  }

  const getStatusLabel = (status: string) => {
    const labels: Record<string, string> = {
      discovered: 'Découvert',
      interested: 'Intéressant',
      applied: 'Candidature envoyée',
      interview: 'Entretien',
      rejected: 'Rejeté',
      archived: 'Archivé'
    }
    return labels[status] || status
  }

  const getWorkModeInfo = (workMode: string | null) => {
    if (!workMode || workMode === 'unknown') return { label: '🏢 Mode inconnu', color: 'gray' }
    
    const modes: Record<string, { label: string, color: string }> = {
      remote: { label: '🏠 Télétravail', color: 'green' },
      hybrid: { label: '🏠🏢 Hybride', color: 'blue' },
      'on-site': { label: '🏢 Présentiel', color: 'orange' }
    }
    
    return modes[workMode] || { label: `🏢 ${workMode}`, color: 'gray' }
  }

  const getFreshnessInfo = (postedAt: string | null) => {
    if (!postedAt) return '📅 Date inconnue'
    
    const posted = new Date(postedAt)
    const now = new Date()
    const diffDays = Math.floor((now.getTime() - posted.getTime()) / (1000 * 60 * 60 * 24))
    
    if (diffDays === 0) return '🔥 Aujourd\'hui'
    if (diffDays <= 3) return `⚡ Il y a ${diffDays}j`
    if (diffDays <= 7) return `📅 Il y a ${diffDays}j`
    return `📅 Il y a ${diffDays}j`
  }

  const handleNotesSubmit = () => {
    onNotesUpdate(job.id, notes)
    close()
  }

  const workModeInfo = getWorkModeInfo(job.work_mode)

  return (
    <>
      <Card shadow="sm" padding="lg" radius="md" withBorder>
        <Stack gap="md">
          {/* Header avec titre et statut */}
          <Group justify="space-between" align="flex-start">
            <div style={{ flex: 1 }}>
              <Text fw={600} size="lg" lineClamp={2} mb={4}>
                {job.title}
              </Text>
              <Group gap="xs" mb="xs">
                <IconBuilding size={14} />
                <Text c="dimmed" size="sm">
                  {job.company_name || 'Entreprise non spécifiée'}
                </Text>
              </Group>
            </div>
            <Badge 
              color={getStatusColor(job.status)}
              variant="light"
              size="sm"
            >
              {getStatusLabel(job.status)}
            </Badge>
          </Group>

          {/* Informations principales */}
          <Stack gap={4}>
            {job.location && (
              <Group gap="xs">
                <IconMapPin size={14} />
                <Text size="sm" c="dimmed">
                  {job.location}
                </Text>
              </Group>
            )}
            
            <Group gap="xs">
              <Text size="sm" color={workModeInfo.color}>
                {workModeInfo.label}
              </Text>
              <Text size="sm" c="dimmed">
                •
              </Text>
              <Text size="sm" c="dimmed">
                {getFreshnessInfo(job.posted_at)}
              </Text>
            </Group>

            {/* Priorité */}
            <Group gap="xs" align="center">
              <Text size="sm" c="dimmed">Priorité:</Text>
              <Rating 
                size="sm"
                value={job.priority}
                onChange={(value) => onPriorityChange(job.id, value)}
              />
            </Group>
          </Stack>

          <Divider />

          {/* Actions */}
          <Group justify="space-between">
            <Group gap="xs">
              {job.source_url && (
                <Button
                  size="xs"
                  variant="light"
                  leftSection={<IconExternalLink size={14} />}
                  onClick={() => window.open(job.source_url!, '_blank')}
                >
                  LinkedIn
                </Button>
              )}
              
              {job.application_url && (
                <Button
                  size="xs"
                  color="green"
                  leftSection={<IconBriefcase size={14} />}
                  onClick={() => window.open(job.application_url!, '_blank')}
                >
                  Postuler
                </Button>
              )}
            </Group>

            <ActionIcon
              size="sm"
              variant="light"
              color="blue"
              onClick={open}
            >
              <IconNotes size={14} />
            </ActionIcon>
          </Group>

          {/* Changement de statut */}
          <Select
            size="xs"
            placeholder="Changer le statut..."
            data={[
              { value: 'interested', label: '⭐ Marquer intéressant' },
              { value: 'applied', label: '📤 Marquer postulé' },
              { value: 'interview', label: '🤝 Entretien programmé' },
              { value: 'rejected', label: '❌ Rejeté' },
              { value: 'archived', label: '📦 Archiver' }
            ]}
            onChange={(value) => value && onStatusChange(job.id, value)}
            clearable
          />

          {/* Notes existantes */}
          {job.notes && (
            <Text size="xs" c="dimmed" style={{ 
              fontStyle: 'italic',
              maxHeight: 40,
              overflow: 'hidden'
            }}>
              📝 {job.notes}
            </Text>
          )}
        </Stack>
      </Card>

      {/* Modal pour les notes */}
      <Modal opened={opened} onClose={close} title={`Notes - ${job.title}`}>
        <Stack>
          <Textarea
            placeholder="Ajoutez vos notes personnelles..."
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            minRows={4}
          />
          <Group justify="flex-end">
            <Button variant="light" onClick={close}>
              Annuler
            </Button>
            <Button onClick={handleNotesSubmit}>
              Sauvegarder
            </Button>
          </Group>
        </Stack>
      </Modal>
    </>
  )
}

// Composant principal Dashboard
export default function Dashboard() {
  const [jobs, setJobs] = useState<JobOffer[]>([])
  const [stats, setStats] = useState<DashboardStats>({
    total_jobs: 0,
    discovered_count: 0,
    interested_count: 0,
    applied_count: 0,
    interview_count: 0,
    remote_count: 0,
    direct_apply_count: 0,
    avg_priority: 0
  })
  const [loading, setLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState('')

  // Chargement initial
  useEffect(() => {
    loadData()
  }, [statusFilter, searchQuery])

  const loadData = async () => {
    try {
      setLoading(true)
      const [jobsData, statsData] = await Promise.all([
        jobOperations.getJobs(statusFilter, 100, searchQuery),
        jobOperations.getDashboardStats()
      ])
      
      setJobs(jobsData)
      setStats(statsData)
    } catch (error) {
      console.error('Error loading data:', error)
      notifications.show({
        title: 'Erreur',
        message: 'Impossible de charger les données',
        color: 'red'
      })
    } finally {
      setLoading(false)
    }
  }

  const handleStatusChange = async (jobId: string, status: string) => {
    try {
      await jobOperations.updateJobStatus(jobId, status)
      notifications.show({
        title: 'Statut mis à jour',
        message: `Emploi marqué comme "${status}"`,
        color: 'green'
      })
      loadData() // Recharger les données
    } catch (error) {
      notifications.show({
        title: 'Erreur',
        message: 'Impossible de mettre à jour le statut',
        color: 'red'
      })
    }
  }

  const handlePriorityChange = async (jobId: string, priority: number) => {
    try {
      await jobOperations.updateJobPriority(jobId, priority)
      // Mise à jour locale immédiate pour une meilleure UX
      setJobs(prev => prev.map(job => 
        job.id === jobId ? { ...job, priority } : job
      ))
    } catch (error) {
      notifications.show({
        title: 'Erreur',
        message: 'Impossible de mettre à jour la priorité',
        color: 'red'
      })
    }
  }

  const handleNotesUpdate = async (jobId: string, notes: string) => {
    try {
      await jobOperations.updateJobNotes(jobId, notes)
      notifications.show({
        title: 'Notes sauvegardées',
        message: 'Les notes ont été mises à jour',
        color: 'green'
      })
      // Mise à jour locale
      setJobs(prev => prev.map(job => 
        job.id === jobId ? { ...job, notes } : job
      ))
    } catch (error) {
      notifications.show({
        title: 'Erreur',
        message: 'Impossible de sauvegarder les notes',
        color: 'red'
      })
    }
  }

  if (loading) {
    return (
      <Center h="100vh">
        <Loader size="lg" />
      </Center>
    )
  }

  return (
    <Container size="xl" py="md">
      {/* Header */}
      <Group justify="space-between" mb="xl">
        <div>
          <Title order={1}>🎯 Job Tracker Simple</Title>
          <Text c="dimmed">
            Suivi personnel des candidatures LinkedIn Enhanced
          </Text>
        </div>
      </Group>

      {/* Statistiques */}
      <StatsCards stats={stats} />

      {/* Filtres */}
      <Paper p="md" mb="xl" withBorder>
        <Grid>
          <Grid.Col span={{ base: 12, md: 6 }}>
            <TextInput
              placeholder="Rechercher par titre ou entreprise..."
              leftSection={<IconSearch size={16} />}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </Grid.Col>
          <Grid.Col span={{ base: 12, md: 6 }}>
            <Select
              placeholder="Filtrer par statut"
              data={[
                { value: 'all', label: 'Tous les emplois' },
                { value: 'discovered', label: 'Découverts' },
                { value: 'interested', label: 'Intéressants' },
                { value: 'applied', label: 'Candidatures envoyées' },
                { value: 'interview', label: 'Entretiens' },
                { value: 'rejected', label: 'Rejetés' },
                { value: 'archived', label: 'Archivés' }
              ]}
              value={statusFilter}
              onChange={(value) => setStatusFilter(value || 'all')}
            />
          </Grid.Col>
        </Grid>
      </Paper>

      {/* Liste des emplois */}
      {jobs.length === 0 ? (
        <Center>
          <Stack align="center" gap="md">
            <Text size="lg" c="dimmed">
              Aucun emploi trouvé
            </Text>
            <Text size="sm" c="dimmed">
              Lancez une synchronisation LinkedIn pour voir vos emplois ici
            </Text>
          </Stack>
        </Center>
      ) : (
        <Grid>
          {jobs.map((job) => (
            <Grid.Col key={job.id} span={{ base: 12, md: 6, lg: 4 }}>
              <JobCard
                job={job}
                onStatusChange={handleStatusChange}
                onPriorityChange={handlePriorityChange}
                onNotesUpdate={handleNotesUpdate}
              />
            </Grid.Col>
          ))}
        </Grid>
      )}
    </Container>
  )
}